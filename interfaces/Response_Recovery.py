
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

from base import Smapi_Request_Base, Obj

class Response_Recovery(Smapi_Request_Base):
    def __init__(self,
                 failed_request_id = 0,
                 **kwargs):
        super(Response_Recovery, self). \
            __init__(b"Response_Recovery", **kwargs)

        # Request values
        self._failed_request_id = failed_request_id

        # Response values
        self._response_data = b""

    @property
    def failed_request_id(self):
        return self._failed_request_id

    @failed_request_id.setter
    def failed_request_id(self, value):
        self._failed_request_id = value

    @property
    def response_data(self):
        return self._response_data

    @response_data.setter
    def response_data(self, value):
        self._response_data = value

    def pack(self):
        # failed_request_id (int4)
        buf = struct.pack("!I", self._failed_request_id)

        return super(Response_Recovery, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Response_Recovery, self).unpack(buf, offset)

        # response_data
        nlen = len(buf) - offset 
        self._response_data = buf[offset:offset + nlen]
        offset += nlen

        return offset

