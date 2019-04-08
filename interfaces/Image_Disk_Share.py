
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

class Image_Disk_Share(Request):
    def __init__(self,
                 image_disk_number = "",
                 target_image_name = "",
                 target_image_disk_number = "",
                 read_write_mode = "",
                 optional_password = "",
                 **kwargs):
        super(Image_Disk_Share, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number
        self._target_image_name = target_image_name
        self._target_image_disk_number = target_image_disk_number
        self._read_write_mode = read_write_mode
        self._optional_password = optional_password

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

    @property
    def read_write_mode(self):
        return self._read_write_mode

    @read_write_mode.setter
    def read_write_mode(self, value):
        self._read_write_mode = value

    @property
    def optional_password(self):
        return self._optional_password

    @optional_password.setter
    def optional_password(self, value):
        self._optional_password = value

    def pack(self):
        idn_len = len(self._image_disk_number)
        tin_len = len(self._target_image_name)
        tidn_len = len(self._target_image_disk_number)
        rwm_len = len(self._read_write_mode)
        op_len = len(self._optional_password)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        # target_image_name_length (int4)
        # target_image_name (string,1-8,char42)
        # target_image_disk_number_length (int4)
        # target_image_disk_number (string,1-4,char16)
        # read_write_mode_length (int4)
        # read_write_mode (string,0-4,char26)
        # optional_password_length (int4)
        # optional_password (string,0-8,charNB)
        fmt = "!I%dsI%dsI%dsI%dsI%dsI%ds" % \
            (idn_len,
             tin_len,
             tidn_len,
             rwm_len,
             op_len)

        buf = struct.pack(fmt,
                          idn_len,
                          bytes(self._image_disk_number, "UTF-8"),
                          sin_len,
                          bytes(self._target_image_name, "UTF-8"),
                          tidn_len,
                          bytes(self._target_image_disk_number, "UTF-8"),
                          rp_len,
                          bytes(self._read_write_mode, "UTF-8"),
                          wp_len,
                          bytes(self._optional_password, "UTF-8"))
 
        return buf

