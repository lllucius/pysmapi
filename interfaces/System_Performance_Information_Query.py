
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

class System_Performance_Information_Query(Smapi_Request_Base):
    def __init__(self,
                 system_performance_information_list = [],
                 **kwargs):
        super(System_Performance_Information_Query, self). \
            __init__(b"System_Performance_Information_Query", **kwargs)

        # Request parameters
        self._system_performance_information_list = system_performance_information_list

        # Response values
        self._system_performance_information_data = []
        self._error_data = []

    @property
    def system_performance_information_list(self):
        return self._system_performance_information_list

    @system_performance_information_list.setter
    def system_performance_information_list(self, value):
        self._system_performance_information_list = value

    @property
    def system_performance_information_data(self):
        return self._system_performance_information_data

    @system_performance_information_data.setter
    def system_performance_information_data(self, value):
        self._system_performance_information_data = value

    @property
    def error_data(self):
        return self._error_data

    @error_data.setter
    def error_data(self, value):
        self._error_data = value

    def pack(self):
        buf = b"\x00".join(self._system_performance_information_list) + b"\x00"

        # system_performance_information_list_length (int4)
        # system_performance_information_list (string,0-maxlength,charNA)
        buf = struct.pack(b"!I", len(buf)) + buf

        return super(System_Performance_Information_Query, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(System_Performance_Information_Query, self).unpack(buf, offset)

        # system_performance_information_data_length (int4)
        # or
        # error_data_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # system_performance_information_data (string)
        # or
        # error_data (string)
        buf = buf[offset:offset + nlen]
        offset += nlen

        if self.return_code == 0 and self.reason_code == 0:
            # system_performance_information_data
            self._system_performance_information_data = buf.split(b"\x00")
        else:
            # error_data
            self._error_data = buf

        return offset

