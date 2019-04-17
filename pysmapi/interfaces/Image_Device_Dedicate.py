
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

class Image_Device_Dedicate(Request):

    # readonly
    FALSE = 0
    TRUE = 1

    def __init__(self,
                 image_device_number = "",
                 real_device_number = "",
                 readonly = FALSE,
                 **kwargs):
        super(Image_Device_Dedicate, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number
        self._real_device_number = real_device_number
        self._readonly = readonly

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def real_device_number(self):
        return self._real_device_number

    @real_device_number.setter
    def real_device_number(self, value):
        self._real_device_number = value

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value

    def pack(self):
        id_len = len(self._image_device_number)
        rd_len = len(self._real_device_number)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)
        # read_device_number_length (int4)
        # real_device_number (string,1-4,char16)
        # readonly (int1)
        fmt = "!I%dsI%dsB" % (id_len, rd_len)
        buf = struct.pack(fmt,
                          id_len,
                          s2b(self._image_device_number),
                          rd_len,
                          s2b(self._real_device_number),
                          self._readonly)
 
        return buf
