
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
