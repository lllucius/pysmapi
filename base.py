
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

import struct

from ctypes import *

class Obj(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        ret = b""
        for key in sorted(self.__dict__):
            if key[0] != "_":
                ret += "%s: %s\n" % (key, self.__dict__[key])
        return ret

class Smapi_Request_Base(object):
    global_authenticated_userid = None
    global_password = None
    def __init__(self,
                 function_name,
                 target = b"",
                 authenticated_userid = None,
                 password = None,
                 **kwargs):

        # Request parameters
        self._function_name = function_name
        self._target = target

        if authenticated_userid is None:
            if self.global_authenticated_userid is None:
                self._authenticated_userid = b""
            else:
                self._authenticated_userid = self.global_authenticated_userid
        else:
            self._authenticated_userid = authenticated_userid

        if password is None:
            if self.global_password is None:
                self._password = b""
            else:
                self._password = self.global_password
        else:
            self._password = password

        # Response values
        self._request_id = 0
        self._return_code = 0
        self._reason_code = 0

    @property
    def function_name(self):
        return self._function_name

    @function_name.setter
    def function_name(self, value):
        self._function_name = value

    @property
    def authenticated_userid(self):
        return self._authenticated_userid

    @authenticated_userid.setter
    def authenticated_userid(self, value):
        self._authenticated_userid = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

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

    def pack(self, extra = b""):
        fn_len = len(self._function_name)
        au_len = len(self._authenticated_userid)
        p_len = len(self._password)
        t_len = len(self._target)

        fmt = b"!I%dsI%dsI%dsI%ds" % (fn_len, au_len, p_len, t_len)
        buf = struct.pack(fmt,
                          fn_len,
                          self._function_name,
                          au_len,
                          self._authenticated_userid,
                          p_len,
                          self._password,
                          t_len,
                          self._target) + extra
        return struct.pack(b"!I", len(buf)) + buf

    def unpack(self, buf, offset):
        return 0

    def request(self, conn, wait=True):
        conn.connect()

        conn.send(self.pack())

        # At this point SMAPI has only accepted the request and hasn't yet
        # acted upon it

        # Get the immediate request ID
        self._request_id, = struct.unpack("!I", conn.recv(4))

        # At this point, SMAPI is processing the request.

        # Get the common response values
        (length,
         self._request_id,
         self._return_code,
         self._reason_code) = struct.unpack("!IIII", conn.recv(16))

        print("REQUEST_ID", self.request_id)
        print("RETURN_CODE", self.return_code)
        print("REASON_CODE", self.reason_code)

        # Remove the common response value length (the length itself isn't included)
        length -= 12

        # Get function specific response data
        if length > 0:
            resp = conn.recv(length)

            print("RESP", resp)
            self.unpack(resp, 0)

        conn.disconnect()

