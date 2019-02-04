
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

class Image_CPU_Define(Smapi_Request_Base):

    # Cpu type
    UNSPECIFIED = 0
    CP = 1
    IFL = 2
    ZAAP = 3
    ZIIP = 4
    cpu_type_names = ["UNSPECIFIED", "CP", "IFL", "ZAAP", "ZIIP"]

    def __init__(self,
                 cpu_address = b"",
                 cpu_type = 0,
                 **kwargs):
        super(Image_CPU_Define, self). \
            __init__(b"Image_CPU_Define", **kwargs)

        # Request parameters
        self._cpu_address = cpu_address
        self._cpu_type = cpu_type

    @property
    def cpu_address(self):
        return self._cpu_address

    @cpu_address.setter
    def cpu_address(self, value):
        self._cpu_address = value

    @property
    def cpu_type(self):
        return self._cpu_address

    @cpu_type.setter
    def cpu_type(self, value):
        self._cpu_type = value

    def pack(self):
        ca_len = len(self._cpu_address)

        # cpu_address_length (int4)
        # cpu_address (string,1-2,char16)
        # cpu_type (int1)
        fmt = b"!I%dsB" % (ca_len)
        buf = struct.pack(fmt,
                          ca_len,
                          self._cpu_address,
                          self._cpu_type)

        return super(Image_CPU_Define, self).pack(buf)

