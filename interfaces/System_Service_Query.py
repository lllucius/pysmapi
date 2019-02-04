
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

class System_Service_Query(Smapi_Request_Base):
    def __init__(self,
                 system_service_query_list = [],
                 **kwargs):
        super(System_Service_Query, self). \
            __init__(b"System_Service_Query", **kwargs)

        # Request parameters
        self._system_service_query_list = system_service_query_list

        # Response values
        self._system_service_query_data = []

    @property
    def system_service_query_list(self):
        return self._system_service_query_list

    @system_service_query_list.setter
    def system_service_query_list(self, value):
        self._system_service_query_list = value

    @property
    def system_service_query_data(self):
        return self._system_service_query_data

    @system_service_query_data.setter
    def system_service_query_data(self, value):
        self._system_service_query_data = value

    def pack(self):
        buf = b""
        for component in self._system_service_query_list:
            buf += component + "\x00"

        # system_service_query_list_length (int4)
        # system_service_query_list (string,1-maxlength,charNA)
        buf = struct.pack(b"!I", len(buf)) + buf

        return super(System_Service_Query, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(System_Service_Query, self).unpack(buf, offset)

        # system_service_query_data_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # system_service_query_data (string) (ASCIIZ ARRAY)
        self._system_service_query_data = buf[offset:offset + alen].split("\x00")
        offset += alen

        return offset

