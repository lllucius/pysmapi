
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

class System_Information_Query(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(System_Information_Query, self). \
            __init__(b"System_Information_Query", **kwargs)

        # Response values
        self._system_information_data = []

    @property
    def system_information_data(self):
        return self._system_information_data

    @system_information_data.setter
    def system_information_data(self, value):
        self._system_information_data = value

    def unpack(self, buf, offset):
        offset = super(System_Information_Query, self).unpack(buf, offset)

        # system_information_data_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # system_information_data (string)
        self._system_information_data = buf[offset:offset + alen].split("\x00")
        offset += alen

        return offset

