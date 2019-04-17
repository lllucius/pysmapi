
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

class Image_Disk_Create(Request):
    def __init__(self,
                 image_disk_number = "",
                 image_disk_mode = "",
                 **kwargs):
        super(Image_Disk_Create, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number
        self._image_disk_mode = image_disk_mode

    @property
    def image_disk_number(self):
        return self._image_disk_number

    @image_disk_number.setter
    def image_disk_number(self, value):
        self._image_disk_number = value

    @property
    def image_disk_mode(self):
        return self._image_disk_mode

    @image_disk_mode.setter
    def image_disk_mode(self, value):
        self._image_disk_mode = value

    def pack(self):
        idn_len = len(self._image_disk_number)
        idm_len = len(self._image_disk_mode)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        # image_disk_mode_length (int4)
        # image_disk_mode (string,0-5,char26)
        fmt = "!I%dsI%ds" % (idn_len, idm_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_disk_number),
                          idm_len,
                          s2b(self._image_disk_mode))
 
        return buf
