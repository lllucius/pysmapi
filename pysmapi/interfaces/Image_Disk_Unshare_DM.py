
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

class Image_Disk_Unshare_DM(Request):
    def __init__(self,
                 image_disk_number = "",
                 target_image_name = "",
                 target_image_disk_number = "",
                 **kwargs):
        super(Image_Disk_Unshare_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number
        self._target_image_name = target_image_name
        self._target_image_disk_number = target_image_disk_number

    @property
    def image_disk_number(self):
        return self._image_disk_number

    @image_disk_number.setter
    def image_disk_number(self, value):
        self._image_disk_number = value

    @property
    def target_image_name(self):
        return self._target_image_name

    @target_image_name.setter
    def target_image_name(self, value):
        self._target_image_name = value

    @property
    def target_image_disk_number(self):
        return self._target_image_disk_number

    @target_image_disk_number.setter
    def target_image_disk_number(self, value):
        self._target_image_disk_number = value

    def pack(self):
        idn_len = len(self._image_disk_number)
        tin_len = len(self._target_image_name)
        tidn_len = len(self._target_image_disk_number)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        # target_image_name_length (int4)
        # target_image_name (string,1-8,char42)
        # target_image_disk_number_length (int4)
        # target_image_disk_number (string,1-4,char16)
        fmt = "!I%dsI%dsI%ds" % \
            (idn_len,
             tin_len,
             tidn_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_disk_number),
                          tin_len,
                          s2b(self._target_image_name),
                          tidn_len,
                          s2b(self._target_image_disk_number))
 
        return buf
