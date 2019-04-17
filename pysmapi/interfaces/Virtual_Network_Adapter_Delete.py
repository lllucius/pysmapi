
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

from pysmapi.smapi import *

class Virtual_Network_Adapter_Delete(Request):
    def __init__(self,
                 image_device_number = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Delete, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    def pack(self):
        idn_len = len(self._image_device_number)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)

        fmt = "!I%ds" % (idn_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_device_number))

        return buf
