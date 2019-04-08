
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

class Image_Unlock_DM(Request):
    def __init__(self,
                 device_address = "",
                 **kwargs):
        super(Image_Unlock_DM, self).__init__(**kwargs)

        # Request parameters
        self._device_address = device_address

    @property
    def device_address(self):
        return self._device_address

    @device_address.setter
    def device_address(self, value):
        self._device_address = value

    def pack(self):
        da_len = len(self._device_address)

        # device_address_length (int4)
        # device_address (string,1-8,char42)
        fmt = "!I%ds" % (da_len)

        buf = struct.pack(fmt,
                          da_len,
                          bytes(self._device_address, "UTF-8"))
 
        return buf
