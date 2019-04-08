
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

class Image_Device_Undedicate_DM(Request):

    # Data security erase
    FALSE = 0
    TRUE = 1
    readonly_names = ["TRUE"]

    def __init__(self,
                 image_device_number = "",
                 **kwargs):
        super(Image_Device_Undedicate_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    def pack(self):
        id_len = len(self._image_device_number)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)
        fmt = "!I%ds" % (id_len)
        buf = struct.pack(fmt,
                          id_len,
                          bytes(self._image_device_number, "UTF-8"))
 
        return buf
