
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

class Image_Disk_Unshare(Request):
    def __init__(self,
                 image_disk_number = "",
                 **kwargs):
        super(Image_Disk_Unshare, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number

    @property
    def image_disk_number(self):
        return self._image_disk_number

    @image_disk_number.setter
    def image_disk_number(self, value):
        self._image_disk_number = value

    def pack(self):
        id_len = len(self._image_disk_number)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        fmt = "!I%ds" % (id_len)
        buf = struct.pack(fmt,
                          id_len,
                          bytes(self._image_disk_number, "UTF-8"))
 
        return buf
