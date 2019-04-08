
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

from pysmapi.smapi import Request, Obj

class Image_CPU_Delete(Request):
    def __init__(self,
                 cpu_address = "",
                 **kwargs):
        super(Image_CPU_Delete, self).__init__(**kwargs)

        # Request parameters
        self._cpu_address = cpu_address

    @property
    def cpu_address(self):
        return self._cpu_address

    @cpu_address.setter
    def cpu_address(self, value):
        self._cpu_address = value

    def pack(self):
        ca_len = len(self._cpu_address)

        # cpu_address_length (int4)
        # cpu_address (string,1-2,char16)
        fmt = "!I%ds" % (ca_len)
        buf = struct.pack(fmt,
                          ca_len,
                          bytes(self._cpu_address, "UTF-8"))

        return buf
