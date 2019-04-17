
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

class Image_Disk_Delete_DM(Request):
    # Data security erase
    UNSPECIFIED = 0
    NOERASE = 1
    ERASE = 2
    data_security_erasure_names = {UNSPECIFIED: "UNSPECIFIED", NOERASE: "NOERASE", ERASE: "ERASE"}

    def __init__(self,
                 image_disk_number = "",
                 data_security_erase = UNSPECIFIED,
                 **kwargs):
        super(Image_Disk_Delete_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number
        self._data_security_erase = data_security_erase

        # Response values
        self._operation_id = 0

    @property
    def image_disk_number(self):
        return self._image_disk_number

    @image_disk_number.setter
    def image_disk_number(self, value):
        self._image_disk_number = value

    @property
    def data_security_erase(self):
        return self._data_security_erase

    @data_security_erase.setter
    def data_security_erase(self, value):
        self._data_security_erase = value

    @property
    def operation_id(self):
        return self._operation_id

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = value

    def pack(self):
        id_len = len(self._image_disk_number)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        # data_security_erase (int1)
        fmt = "!I%dsB" % (id_len)
        buf = struct.pack(fmt,
                          id_len,
                          s2b(self._image_disk_number),
                          self._data_security_erase)
 
        return buf
        
    def unpack(self, buf):
        offset = 0

        # operation_id (int4; range -1-2147483647)
        self._operation_id, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

