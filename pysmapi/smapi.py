
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# openssl s_client -showcerts -connect vm1:44446 </dev/null 2>&1 | sed -e '/BEGIN CERT/,/END CERT/p;d'

from ctypes import *
from ctypes.util import find_library
from fnmatch import fnmatch
from select import select
from time import sleep

import errno
import socket
import ssl
import struct
import hexdump

# Number of seconds to sleep while polling for async request completion
INTERVAL = 1

# Maximum number of seconds to wait while sending/receiving
TIMEOUT = 30

# ==============================================================================
# Enable/Disable debugging
# ==============================================================================
debugging = False
def set_debug(enable = True):
    global debugging
    debugging = enable

# ==============================================================================
# Enable/Disable testing
# ==============================================================================
testing = False
def set_test(enable = True):
    global testing
    testing = enable

# ==============================================================================
# Encode data going to SMAPI
# ==============================================================================
def s2b(str):
    return bytes(str, "ISO-8859-15")

# ==============================================================================
# Decode data coming from SMAPI
# ==============================================================================
def b2s(array):
    return array.decode("ISO-8859-15")

# ==============================================================================
# Generic class used for dynamic object creation
# ==============================================================================
class Obj(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        ret = ""

        have_indent = "_indent" in self.__dict__
        if not have_indent:
            self._indent = 0

        for key in self.__dict__:
            val = self.__dict__[key]

            if key[0] != "_":
                ret += (" " * self._indent) + f"{key}: "

                if isinstance(val, list):
                    ret += "\n"

                    for item in val:
                        if isinstance(item, Obj):
                            item._indent += 4

                        for line in f"{item}".split("\n"):
                            ret += (" " * self._indent) + f"{line}\n"

                        if isinstance(item, Obj):
                            item._indent -= 4
                else:
                    ret += f"{val}\n"

        if not have_indent:
            del self._indent

        return ret

# ==============================================================================
# Host Information
# ==============================================================================
class HostInfo(object):
    def __init__(self, iucv=False, host=None, port=44444, userid=None, password=None, ssl=False, insecure=False, cert=None, timeout=TIMEOUT):
        if iucv is not True and iucv is not False:
            raise ValueError("iucv must be True or False")

        if userid is not None and password is None:
            raise ValueError("password required when userid given")
        if userid is None and password is not None:
            raise ValueError("userid required when password given")

        if ssl is not True and ssl is not False:
            raise ValueError("ssl must be True or False")

        if insecure is not True and insecure is not False:
            raise ValueError("insecure must be True or False")

        if iucv:
            self._libc = CDLL(find_library(b"c"), use_errno=True)
        else:
            if host is None or port is None:
                raise ValueError("host and port required for inet connections")
            if userid is None or password is None:
                raise ValueError("userid and password required for inet connections")

        self._iucv = iucv
        self._host = host
        self._port = port
        self._userid = userid
        self._password = password
        self._ssl = ssl
        self._insecure = insecure
        self._cert = cert
        self._timeout = timeout

    @property
    def iucv(self):
        return self._iucv

    @iucv.setter
    def iucv(self, value):
        self._iucv = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, value):
        self._userid = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def ssl(self):
        return self._ssl

    @ssl.setter
    def ssl(self, value):
        self._ssl = value

    @property
    def cert(self):
        return self._cert

    @cert.setter
    def cert(self, value):
        self._cert = value

    @property
    def insecure(self):
        return self._insecure

    @insecure.setter
    def insecure(self, value):
        self._insecure = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

# ==============================================================================
# IUCV structure used for IUCV connections
# ==============================================================================
class IUCV(Structure):
    AF_IUCV = 32

    _fields_ = [
        (u"siucv_family", c_ushort),
        (u"siucv_port", c_ushort),
        (u"siucv_addr", c_uint),
        (u"siucv_nodeid", c_char * 8),
        (u"siucv_user_id", c_char * 8),
        (u"siucv_name", c_char * 8)
    ]

    def __init__(self, user = "VSMREQIU", name = "DMSRSRQU"):
        super(IUCV, self).__init__()

        self.siucv_family = AF_IUCV
        self.siucv_port = 0
        self.siucv_addr = 0
        self.siucv_nodeid = b" " * 8
        self.siucv_user_id = b" " * 8 if user is None else user.ljust(8)
        self.siucv_name = b" " * 8 if name is None else name.ljust(8)

    @property
    def siucv_user_id(self):
        return self.siucv_user_id.rstrip()

    @siucv_user_id.setter
    def siucv_user_id(self, value):
        if len(value) > 8:
            raise ValueError("siucv_user_id is longer than 8 characters")
        self.siucv_user_id = value.ljust(8)

    @property
    def siucv_name(self):
        return self.siucv_name.rstrip()

    @siucv_name.setter
    def siucv_name(self, value):
        if len(value) > 8:
            raise ValueError("siucv_name is longer than 8 characters")
        self.siucv_name = value.ljust(8)

# ==============================================================================
# Request Base 
# ==============================================================================
class Request(object):
    def __init__(self,
                 target = "",
                 **kwargs):

        # Request parameters
        self._function_name = self.__class__.__name__
        self._target = target

        # Response values
        self._request_id = 0
        self._return_code = 0
        self._reason_code = 0

        # Capture buffers for testing
        self._send = b""
        self._recv = b""

    def request(self, hostinfo, wait=True, interval=INTERVAL):
        # Save host info
        self._hinfo = hostinfo

        # Get the request
        _req = self
        opid = None
        cont = True

        # Response values
        _req._request_id = 0
        _req._return_code = 0
        _req._reason_code = 0

        while cont:
            # If we have an operation id, then we're waiting for an async
            # operation to complete.  We need to pause for the given interval.
            if opid is not None:
                # Wait for the given interval
                sleep(interval)

            # Get request specific parameters
            buf = _req.pack()

            # Must connect to the SMAPI host for each request
            _req.connect()

            # Send the request
            _req.send(buf)

            # At this point SMAPI has only accepted the request and hasn't yet
            # acted upon it

            # Get the immediate request ID
            _req._request_id, = struct.unpack("!I", _req.recv(4))

            # At this point, SMAPI is processing the request.

            # Get the common response values
            (length,
             _req._request_id,
             _req._return_code,
             _req._reason_code) = struct.unpack("!IIII", _req.recv(16))

            if debugging:
                print("REQUEST_ID", _req.request_id)
                print("RETURN_CODE", _req.return_code)
                print("REASON_CODE", _req.reason_code)

            # Remove the common response value length (the length itself isn't included)
            length -= 12

            # Does caller want to wait for async operation completion?
            if wait:
                # Was an async operation started?
                if _req._return_code == 592:
                    # Grab operation ID if this is a real async operation
                    if _req._reason_code == 0 and length == 4:
                        opid, = struct.unpack("!I", _req.recv(length))

                        # If we're testing, the operation id and return code must
                        # be removed from the buffer.
                        if testing:
                            _req._recv = _req._recv[:12] + \
                                         struct.pack("!IIi", 0, 0, 0)

                    # Otherwise, the operation ID is the reason code 
                    elif _req._reason_code != 0:
                        opid = _req._reason_code

                    # Create query request if we have an operation ID
                    if opid is not None:
                        # Disconnect from current connection
                        _req.disconnect()

                        # Import is done here to resolve circular dependency problem.
                        from pysmapi.interfaces import Query_Asynchronous_Operation_DM

                        # Setup new request
                        _req = Query_Asynchronous_Operation_DM()
                        _req._hinfo = self._hinfo
                        _req.target = self._target
                        _req.operation_id = opid

                        # Go check for completion
                        continue

                # Is the operation still active?
                if _req._return_code == 0 and _req._reason_code == 104:
                    # Disconnect from current connection
                    _req.disconnect()

                    # Go check again
                    continue

                # Async operation has completed
                if _req._return_code == 0 and _req._reason_code == 100:
                    # Set final reason codes
                    _req._reason_code = 0

                self._return_code = _req._return_code
                self._reason_code = _req._reason_code

            # Get function specific response data
            if length > 0:
                resp = _req.recv(length)

                if debugging:
                    print("RESP:")
                    hexdump.hexdump(resp)

                # Unpack and store the response
                _req.unpack(resp)

            # Done with this connection
            _req.disconnect()

            # Exit from loop
            cont = False

        if testing:
            # Get rid of stuff we don't need
            del self._hinfo
            del self._socket

            # Remove request ids from received data
            self._recv = (b"\x00\x00\x00\x00" +
                          self._recv[4:8] + 
                          b"\x00\x00\x00\x00" +
                          self._recv[12:])
            self._request_id = 0

        return self

    @property
    def function_name(self):
        return self._function_name

    @function_name.setter
    def function_name(self, value):
        self._function_name = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def request_id(self):
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        self._request_id = value

    @property
    def return_code(self):
        return self._return_code

    @return_code.setter
    def return_code(self, value):
        self._return_code = value

    @property
    def reason_code(self):
        return self._reason_code

    @reason_code.setter
    def reason_code(self, value):
        self._reason_code = value

    def pack(self):
        return b""

    def unpack(self, buf):
        return

    def connect(self):
        if self._hinfo.iucv:
            sa = IUCV()

            self._fd = self._hinfo._libc.socket(IUCV.AF_IUCV, socket.SOCK_STREAM, socket.IPPROTO_IP)
            errno = get_errno()
            if self._fd == -1:
                raise IOError(errno, "Failed to create IUCV socket")

            ret = self._hinfo._libc.bind(self._fd, sa, sizeof(sa))
            errno = get_errno()
            if ret == -1:
                raise IOError(errno, "Unable to bind IUCV socket")

            ret = self._hinfo._libc.connect(self._fd, sa, sizeof(sa))
            errno = get_errno()
            if ret == -1:
                raise IOError(errno, "Failed to establish IUCV connection")

            # Duplicates the fd and creates a new socket object
            self._socket = socket.fromfd(self._fd, IUCV.AF_IUCV, socket.SOCK_STREAM, socket.IPPROTO_IP)
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self._hinfo.ssl:
                #self.sslctx = ssl.create_default_context()

                self._sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                self._sslctx.check_hostname = False
#                self._sslctx.verify_mode = ssl.CERT_NONE
                self._sslctx.verify_mode = ssl.CERT_REQUIRED
                self._sslctx.load_verify_locations("/root/cert")
                self._socket = self.sslctx.wrap_socket(self._socket) #, server_hostname=self.inet[0])

            self._socket.connect((self._hinfo.host, self._hinfo.port))

    def disconnect(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        self._socket = None

        # For IUCV, close the original file descriptor as well to make sure the
        # connection is dropped otherwise it can't be reconnected.
        if self._hinfo.iucv:
            self._hinfo._libc.close(self._fd)

    def send(self, buf):
        # Build common parameters
        fn_len = len(self._function_name)
        au_len = len(self._hinfo.userid)
        p_len = len(self._hinfo.password)
        t_len = len(self._target)

        # function_name_length (int4)
        # function_name (string,27,char43)
        # authenticated_userid_length (int4)
        # authenticated_userid (string,1-8,char42)
        #                      (string,0-8,char42)
        # password_length (int4)
        # password (string,1-200,charNA)
        #          (string,0-200,charNA)
        # target_identifier_length (int4)
        # target_identifier (string,1-8,char42)
        fmt = b"!I%dsI%dsI%dsI%ds" % (fn_len, au_len, p_len, t_len)
        buf = struct.pack(fmt,
                          fn_len,
                          s2b(self._function_name),
                          au_len,
                          s2b(self._hinfo.userid),
                          p_len,
                          s2b(self._hinfo.password),
                          t_len,
                          s2b(self._target)) + buf

        # Prepend the total length
        buf = struct.pack(b"!I", len(buf)) + buf

        if testing:
            self._send += buf

        if debugging:
            print("SEND:")
            hexdump.hexdump(buf)

        index = 0
        length = len(buf)

        while length > 0:
            _, wlist, _ = select([], [self._socket], [], self._hinfo.timeout)
            if len(wlist) == 0:
                raise IOError(errno.ETIMEDOUT, "Timed out waiting to send %d bytes", length)
            sent = self._socket.send(buf[index:length])

            length -= sent
            index += sent

    def recv(self, length):
        buf = b""

        while length > 0:
            rlist, _, _ = select([self._socket], [], [], self._hinfo.timeout)
            if len(rlist) == 0:
                raise IOError(errno.ETIMEDOUT, f"Timed out waiting to receive {length} bytes")

            read = self._socket.recv(length)
            if len(read) == 0:
                raise IOError(errno.ENOTCONN, "Connection closed by remote")

            buf += read
            length -= len(read)

        if debugging:
            print("RECV:")
            hexdump.hexdump(buf)

        if testing:
            self._recv += buf

        return buf

    def error_string(self):
        errs = \
        {
            # RC_OK
            "0_0_Query_API_Functional_Level": "The API functional level is z/VM V5.3",
            "0_0_*": "Request successful",
            "0_4_Shared_Memory_Create": "Segment was created, but specified userid could not be found to give RSTD access",
            "0_4_Shared_Memory_Replace": "Segment was replaced, but specified userid could not be found to give RSTD access",
            "0_4_Image_CPU_Define": "CPU defined, but CPU affinity suppressed",
            "0_8_*": "Request successful; object directory offline",
            "0_12_Name_List_Add": "Request successful; new list created",
            "0_12_Shared_Memory_*": "Request successful; NAMESAVE statement already exists in directory",
            "0_12_*": "Image not active",
            "0_16_*": "Request successful; no more entries, list destroyed",
            "0_20_Directory_Manager_Local_Tag_Set_DM": "Use not allowed by exit routine.",
            "0_20_*": "No output; user(s) not authorized for specified segment",
            "0_24_*": "Request successful; virtual network LAN removed",
            "0_28_Image_SCSI_Characteristics_Query_DM": "There are no SCSI characteristics for this image.",
            "0_28_Shared_Memory_Query": "Query request successful, but segment not found",
            "0_28_Asynchronous_Notification_*": "No matching entries found",
            "0_28_*": "No matching entries found.  Return buffer is empty.",
            "0_32_*": "Name was not in list",
            "0_36_*": "Name is already in list",
            "0_40_*": "Request successful; new virtual switch created",
            "0_44_*": "Request successful; virtual switch removed",
            "0_66_*": "Multiple DEFINE or MODIFY statements are erased in system config",
            "0_100_*": "Asynchronous operation succeeded",
            "0_104_*": "Asynchronous operation in progress",
            "0_108_*": "Asynchronous operation failed",
            "0_540_*": "The API functional level is z/VM V5.4",
            "0_610_*": "The API functional level is z/VM V6.1",

            # RC_WNG
            "4_5_*": "Unrestricted LAN",
            "4_6_*": "No authorized users",

            # RC_ERR
            "8_2_*": "Invalid access user",
            "8_3_*": "Invalid op value",
            "8_4_*": "Invalid promiscuity value",
            "8_2783_*": "Invalid LAN ID",
            "8_2795_*": "Invalid LAN parameter",

            # RCERR_FILE_NOT_FOUND
            "28_0_*": "Namelist file not found",

            # RCERR_FILE_CANNOT_BE_UPDATED
            "36_0_*": "Namelist file cannot be updated",

            # RCERR_AUTH
            "100_0_*": "Request is authorized",
            "100_4_*": "Authorization deferred to directory manager",
            "100_8_*": "Request not authorized by external security manager",
            "100_12_*": "Request not authorized by directory manager",
            "100_16_*": "Request not authorized by server",
            "100_20_*": "Target image not authorized for function",

            # RCERR_NO_AUTHFILE
            "104_0_*": "Authorization file not found",

            # RCERR_AUTHFILE_RO
            "106_0_*": "Authorization file cannot be updated",

            # RCERR_EXISTS
            "108_0_*": "Authorization file entry already exists",

            # RCERR_NO_ENTRY
            "112_0_*": "Authorization file entry does not exist",

            # RCERR_USER_PW_BAD
            "120_0_*": "Authentication error; userid or password not valid",

            # RCERR_PW_EXPIRED
            "128_0_*": "Authentication error; password expired",

            # RCERR_ESM
            "188_*": "Internal server error; ESM failure: {reas}",

            # RCERR_PW_CHECK
            "192_*": "Internal server error; cannot authenticate user/password: {reas}",

            # RCERR_IMAGEOP
            "200_0_*": "Image operation error",
            "200_4_*": "Image not found",
            "200_8_*": "Image already active",
            "200_12_*": "Image not active",
            "200_16_*": "Image being deactivated",
            "200_24_*": "List not found",
            "200_28_*": "Some images in list not activated",
            "200_32_*": "Some images in list not deactivated",
            "200_36_Image_Recycle": "Some images in list not recycled",
            "200_36_Image_Deactivate": "Specified time results in interval greater than max allowed",

            # RCERR_IMAGEDEVU
            "204_0_*": "Image device usage error",
            "204_4_*": "Image device already exists",
            "204_8_*": "Image device does not exist",
            "204_12_*": "Image device is busy",
            "204_16_*": "Image device is not available",
            "204_20_*": "Image device already connected",
            "204_24_*": "Image device is not a tape drive, or cannot be assigned/reset",
            "204_28_*": "Image device is not a shared DASD",
            "204_32_*": "Image device is not a reserved DASD",
            "204_36_*": "I/O error on image device",
            "204_40_*": "Virtual Network Adapter not deleted",
            "204_44_*": "DASD volume cannot be deleted",
            "204_48_*": "Virtual network adapter is already disconnected",

            # RCERR_IMAGEDISKU
            "208_0_*": "Image disk usage error",
            "208_4_*": "Image disk already in use",
            "208_8_*": "Image disk not in use",
            "208_12_*": "Image disk not available",
            "208_16_*": "Image disk cannot be shared as requested",
            "208_20_*": "Image disk shared in different mode",
            "208_28_*": "Image disk does not have",
            "208_32_*": "Incorrect password specified for image disk",
            "208_36_*": "Image disk does not exist",
            "208_1157_*": "MDISK DEVNO parameter requires the device to be a free volume",

            # RCERR_IMAGECONN
            "212_0_*": "Active image connectivity error",
            "212_4_*": "Partner image not found",
            "212_8_Virtual_Network_Adapter_Query": "Adapter does not exist",
            "212_8_*": "Image not authorized to connect",
            "212_12_*": "LAN does not exist",
            "212_16_*": "LAN owner LAN name does not exist",
            "212_20_*": "Requested LAN owner not active",
            "212_24_*": "LAN name already exists with different attributes",
            "212_28_*": "Image device not correct type for requested connection",
            "212_32_*": "Image device not connected to LAN",
            "212_36_*": "Virtual switch already exists",
            "212_40_*": "Virtual switch does not exist",
            "212_44_*": "Image already authorized",
            "212_52_*": "Maximum number of connections reached",
            "212_96_*": "Unknown reason",

            # RCERR_IMAGECPU
            "216_2_*": "Input virtual CPU value out range",
            "216_4_*": "Virtual CPU not found",
            "216_12_*": "Image not active",
            "216_24_*": "Virtual CPU already exists",
            "216_28_*": "Virtual CPU address beyond allowable range defined in directory",
            "216_40_*": "Processor type not supported on your system",

            # RCERR_VOLUME
            "300_0_*": "Image volume operation successful",
            "300_8_*": "Device not found",
            "300_10_*": "Device not available for attachment",
            "300_12_*": "Device not a volume",
            "300_14_*": "Free modes not available",
            "300_16_*": "Device vary online failed",
            "300_18_*": "Volume label not found in system configuration",
            "300_20_*": "Volume label already in system configuration",
            "300_22_*": "Parm disks 1 and 2 are same",
            "300_24_*": "Error linking parm disk (1 or 2)",
            "300_28_*": "Parm disk (1 or 2) not RW",
            "300_32_*": "System configuration not found on parm disk 1",
            "300_34_*": "System configuration has bad data",
            "300_36_*": "Syntax errors updating system configuration file",
            "300_38_*": "CP disk modes not available",
            "300_40_*": "Parm disk (1 or 2) is full",
            "300_42_*": "Parm disk (1 or 2) access not allowed",
            "300_44_*": "Parm disk (1 or 2) PW not supplied",
            "300_46_*": "Parm disk (1 or 2) PW is incorrect",
            "300_48_*": "Parm disk (1 or 2) is not in server's user directory",
            "300_50_*": "Error in release of CPRELEASE parm disk (1 or 2)",
            "300_52_*": "Error in access of CPACCESS parm disk (1 or 2)",

            # RCERR_INTERNAL
            "396_0_*": "Internal system error",
            "396_*": "Internal system error - product-specific return code (try HELP HCP{reas:%03d}E in CMS)",

            # RCERR_IMAGEDEF
            "400_0_*": "Image or profile definition error",
            "400_4_*": "Image or profile definition not found",
            "400_8_*": "Image or profile name already defined",
            "400_12_*": "Image or profile definition is locked",
            "400_16_*": "Image or profile definition cannot be deleted",
            "400_20_*": "Image prototype is not defined",
            "400_24_*": "Image or profile definition is not locked",
            "400_40_*": "Multiple user statements",

            # RCERR_IMAGEDEVD
            "404_0_*": "Image device definition error",
            "404_4_*": "Image device already defined",
            "404_8_*": "Image device not defined",
            "404_12_*": "Image device is locked",
            "404_24_Image_Disk_Copy_DM": "Image device type not same as source",
            "404_24_*": "Image device is not locked",
            "404_28_*": "Image device size not same as source",

            # RCERR_IMAGEDISKD
            "408_0_*": "Image disk definition error",
            "408_4_*": "Image disk already defined",
            "408_8_*": "Image disk not defined",
            "408_12_*": "Image device is locked",
            "408_16_*": "Image disk sharing not allowed by target image definition",
            "408_24_*": "Requested image disk space not available",
            "408_28_*": "Image disk does not have required password",
            "408_32_*": "Incorrect password specified for image disk",

            # RCERR_IMAGECONND
            "412_0_*": "Image connectivity definition error",
            "412_4_*": "Partner image not found",
            "412_16_*": "Parameters do not match existing directory statement",
            "412_28_*": "Image device not correct type for requested connection",

            # RCERR_PROTODEF
            "416_0_*": "Prototype definition error",
            "416_4_*": "Prototype definition not found",
            "416_8_*": "Prototype already exists",

            # RC_DASD_DM
            "420_4_*": "Group, region, or volume name is already defined",
            "420_8_*": "Group, region, or volume name is not defined",
            "420_12_*": "Region name is not included in the group",
            "420_36_*": "The requested volume is offline or is not a DASD device",

            # RCERR_SEGMENT_DM
            "424_4_*": "Namesave statement already exists",
            "424_8_*": "Segment name not found",

            # RCERR_NOTIFY
            "428_4_*": "Duplicate subscription",
            "428_8_*": "No matching entries",

            # RCERR_TAG
            "432_4_*": "Tag name is already defined",
            "432_8_*": "Tag name is not defined",
            "432_12_*": "Tag ordinal is already defined",
            "432_16_Directory_Manager_Local_Tag_Set_DM": "Tag too long",
            "432_16_*": "Tag is in use in one or more directory entries, can not be revoked",
            "432_20_*": "Use not allowed by exit routine",

            # RCERR_PROFILED
            "436_4_*": "Profile included not found",
            "436_40_*": "Multiple profiles included",

            # RCERR_POLICY_PW
            "444_0_*": "Password policy error",
            "444_4_*": "Password too long",
            "444_8_*": "Password too short",
            "444_12_*": "Password content does not match policy",

            # RCERR_POLICY_ACCT
            "448_0_*": "Account policy error",
            "448_4_*": "Account number too long",
            "448_8_*": "Account number too short",
            "448_12_*": "Account number content does not match policy",

            # RCERR_TASK
            "452_4_*": "Task not found",

            # RCERR_SCSI
            "456_4_*": "LOADDEV statement not found",

            # RC_IPL_DM
            "460_4_*": "Image does not have an IPL statement",

            # RCERR_DM
            "500_0_*": "Directory manager request could not be completed",
            "500_4_*": "Directory manager is not accepting updates",
            "500_8_*": "Directory manager is not available",
            "500_12_*": "Directory manager has been disabled",
            "500_16_*": "Directory manager was interrupted",
            "500_20_*": "Password format not supported",

            # RCERR_LIST_DM
            "504_*": "Target ID not added - product-specific return code: {reas}",

            # RCERR_CPU_DM
            "520_24_*": "Only one base CPU may be defined",
            "520_28_*": "Input virtual CPU value out of range",
            "520_30_*": "CPU not found",
            "520_32_*": "Maximum allowable number of virtual CPUs is exceeded",
            "520_45_*": "The Cryptographic Coprocessor Facility (CCF) is not installed on this system",
            "520_282_*": "SCPDATA contains invalid UTF-8 data",

            # RCERR_ASYNC_DM
            "592_0_*": "Asynchronous operation started",
            "592_*": "Asynchronous operation started - product-specific asynchronous operation ID: {reas}",

            # RCERR_INTERNAL_DM
            "596_*": "Internal directory manager error - product-specific return code: {reas}",

            # RCERR_SHSTOR
            "600_8_*": "Bad page range",
            "600_12_*": "User not logged on",
            "600_16_*": "Could not save segment",
            "600_20_*": "Not authorized to issue internal system command or is not authorized for RSTD segment",
            "600_24_*": "Conflicting parameters",
            "600_28_*": "Segment not found or does not exist",
            "600_299_*": "Class S (skeleton) segment file already exists",

            # RCERR_VIRTUALNETWORKD
            "620_14_*": "Free modes not available",
            "620_22_*": "System config parm disks 1 and 2 are same",
            "620_24_*": "Error linking parm disk (1 or 2)",
            "620_28_*": "Parm disk (1 or 2) not RW",
            "620_32_*": "System config not found on parm disk 1",
            "620_34_*": "System config has bad data",
            "620_36_*": "Syntax errors updating system config",
            "620_38_*": "CP disk modes not available",
            "620_40_*": "Parm disk (1 or 2) is full",
            "620_42_*": "Parm disk (1 or 2) access not allowed",
            "620_44_*": "Parm disk (1 or 2) PW not supplied",
            "620_46_*": "Parm disk (1 or 2) PW is incorrect",
            "620_48_*": "Parm disk (1 or 2) is not in server's directory",
            "620_50_*": "Error in release of CPRELEASE parm disk (1 or 2)",
            "620_52_*": "Error in access of CPACCESS parm disk (1 or 2)",
            "620_54_*": "DEFINE VSWITCH statement already exists in system config",
            "620_58_*": "MODIFY VSWITCH statement to userid not found in system config",
            "620_60_*": "DEFINE VSWITCH statement does not exist in system config",
            "620_62_*": "DEFINE operands conflict, cannot be updated in the system config",
            "620_64_*": "Multiple DEFINE or MODIFY statements found in system config",

            # RCERR_VMRM
            "800_8_*": "No measurement data exists",
            "800_12_*": "Error in update buffer or processing syntax check",
            "800_16_*": "Not authorized to access file",
            "800_24_*": "Error writing file(s) to directory",
            "800_28_*": "Specified configuration file not found",
            "800_32_*": "Internal error processing updates",

            # RCERR_SERVER
            "900_4_*": "Custom exec not found",
            "900_8_*": "Worker server was not found",
            "900_12_*": "Specified function does not exist",
            "900_16_*": "Internal server error - DMSSIPTS entry for function is invalid",
            "900_20_*": "Total length does not match the specified input data",
            "900_24_*": "Error accessing SFS directory",
            "900_28_*": "Internal server error - error with format of function output",
            "900_32_*": "Internal server error - response from worker server was not valid",
            "900_36_*": "Specified length was not valid, out of valid server data range",
            "900_40_*": "Internal server socket error"
        }

        msg = None

        # Try generic checks first
        for t in [f"{self.return_code}_{self.reason_code}_{self.function_name}",
                  f"{self.return_code}_{self.reason_code}_*",
                  f"{self.return_code}_*"]:
            if t in errs:
                msg = errs[t].format(reas=self.reason_code)
                break

        # Handle RCERR_SYNTAX return code
        if not msg and self.return_code == 24:
            rsns = \
            {
                 1: "First character of listname is a colon \":\"",
                10: "Characters not \"0123456789\"",
                11: "Unsupported function",
                13: "Length is greater than maximum or exceeds total length",
                14: "Length is less than minimum",
                15: "Numeric value less than minimum or null value encountered",
                16: "Characters not \"0123456789ABCDEF\"",
                17: "Characters not \"0123456789ABCDEF-\"",
                18: "Numeric value greater than maximum",
                19: "Unrecognized value",
                23: "Conflicting parameter specified",
                24: "Unspecified required parameter",
                25: "Extraneous parameter specified",
                26: "Characters not \"ABCDEFGHIJKLMNOPQRSTUVWXYZ\"",
                36: "Characters not \"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"",
                37: "Characters not \"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-\"",
                42: "Characters not \"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$+-:\"",
                43: "Characters not \"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$+-:_\"",
                44: "Characters not \"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$+-:_=\"",
                45: "Invalid SFS syntax",
                88: "Unexpected end of data",
                99: "Non-breaking characters: non-blank, non-null, non-delete, non-line-end, non-carriage return, non-line-feed"
            }
            pp = self.reason_code / 100
            rr = self.reason_code % 100
            if rr in rsns:
                msg = f"Syntax error in parameter {pp}: {rsns[rr]}"
            else:
                msg = f"Unknown syntax error {rr} in parameter {pp}"

        # Glob search for a match
        if not msg:
            srch = f"{self.return_code}_{self.reason_code}_{self.function_name}"
            for key in errs:
                if fnmatch(srch, key):
                    msg = errs[key]
                    break

        # Give up and produce a generic message
        if not msg:
            msg = f"RC={self.return_code} and RS={self.reason_code}"

        return f"{self.function_name} failed with: {msg}"

