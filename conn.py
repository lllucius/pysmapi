
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

from ctypes import *
from ctypes.util import find_library
from select import select
import errno
import struct
import socket

TIMEOUT = 30
AF_IUCV = 32
SOCK_STREAM = 1
SOCK_NONBLOCK = 2048
SHUT_RDWR = 2
IPPROTO_IP = 0

class SockAddr_IUCV(Structure):
    _fields_ = [
        (b"siucv_family", c_ushort),
        (b"siucv_port", c_ushort),
        (b"siucv_addr", c_uint),
        (b"siucv_nodeid", c_char * 8),
        (b"siucv_user_id", c_char * 8),
        (b"siucv_name", c_char * 8)
    ]

    def __init__(self, user = None, name = None):
        super(SockAddr_IUCV, self).__init__()

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
            raise ValueError(b"siucv_user_id is longer than 8 characters")
        self.siucv_user_id = value.ljust(8)

    @property
    def siucv_name(self):
        return self.siucv_name.rstrip()

    @siucv_name.setter
    def siucv_name(self, value):
        if len(value) > 8:
            raise ValueError(b"siucv_name is longer than 8 characters")
        self.siucv_name = value.ljust(8)

class Smapi_Conn(object):
    def __init__(self, iucv=None, inet=None, timeout=TIMEOUT):
        if iucv is not None and inet is not None:
            raise ValueError(b"iucv and inet parameters may not be used togethered")

        if iucv is not None:
            if len(iucv) != 2 or iucv[0] is None or iucv[1] is None:
                raise ValueError(b"iucv tuple requires the user and name parameters")

            self.libc = CDLL(find_library(b"c"), use_errno=True)
        elif inet is not None:
            if len(inet) != 2 or inet[0] is None or inet[1] is None:
                raise ValueError(b"inet tuple requires the host and port parameters")

        self.iucv = iucv
        self.inet = inet
        self.timeout = timeout

    def connect(self):
        if self.iucv is not None:
            user, name = self.iucv

            sa = SockAddr_IUCV(user=user, name=name)

            self.fd = self.libc.socket(AF_IUCV, SOCK_STREAM, IPPROTO_IP)
            errno = get_errno()
            if self.fd == -1:
                raise IOError(errno, "Failed to create IUCV socket")

            ret = self.libc.bind(self.fd, sa, sizeof(sa))
            errno = get_errno()
            if ret == -1:
                raise IOError(errno, "Unable to bind IUCV socket")

            ret = self.libc.connect(self.fd, sa, sizeof(sa))
            errno = get_errno()
            if ret == -1:
                raise IOError(errno, "Failed to establish IUCV connection")

            # Duplicates the fd and creates a new socket object
            self.socket = socket.fromfd(self.fd, AF_IUCV, SOCK_STREAM, IPPROTO_IP)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.inet)

    def disconnect(self):
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        self.socket = None

        # For IUCV, close the original file descriptor as well to make sure the
        # connection is dropped otherwise it can't be reconnected.
        if self.iucv is not None:
            self.libc.close(self.fd)

    def send(self, buf):
        print("SEND", buf)
        index = 0
        length = len(buf)

        while length > 0:
            _, wlist, _ = select([], [self.socket], [], self.timeout)
            if len(wlist) == 0:
                raise IOError(errno.ETIMEDOUT, "Timed out waiting to send %d bytes", length)
            sent = self.socket.send(buf[index:length])

            length -= sent
            index += sent

    def recv(self, length):
        buf = b""

        while length > 0:
            rlist, _, _ = select([self.socket], [], [], self.timeout)
            if len(rlist) == 0:
                raise IOError(errno.ETIMEDOUT, "Timed out waiting to receive %d bytes", length)

            read = self.socket.recv(length)
            #print(b"READ", read)

            if len(read) == 0:
                raise IOError(errno.ENOTCONN, "Connection closed by remote")

            buf += read
            length -= len(read)
        #print("RECV", buf)
        return buf
