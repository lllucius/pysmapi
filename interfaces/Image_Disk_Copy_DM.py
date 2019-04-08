
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

class Image_Disk_Copy_DM(Request):
    def __init__(self,
                 image_disk_number = "",
                 source_image_name = "",
                 source_image_disk_number = "",
                 image_disk_allocation_type = "",
                 allocation_area_name_or_volser = "",
                 image_disk_mode = "",
                 read_password = "",
                 write_password = "",
                 multi_password = "",
                 **kwargs):
        super(Image_Disk_Copy_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number
        self._source_image_name = source_image_name
        self._source_image_disk_number = source_image_disk_number
        self._image_disk_allocation_type = image_disk_allocation_type
        self._allocation_area_name_or_volser = allocation_area_name_or_volser
        self._image_disk_mode = image_disk_mode
        self._read_password = read_password
        self._write_password = write_password
        self._multi_password = multi_password

        # Response values
        self._operation_id = 0

    @property
    def image_disk_number(self):
        return self._image_disk_number

    @image_disk_number.setter
    def image_disk_number(self, value):
        self._image_disk_number = value

    @property
    def source_image_name(self):
        return self._source_image_name

    @source_image_name.setter
    def source_image_name(self, value):
        self._source_image_name = value

    @property
    def source_image_disk_number(self):
        return self._source_image_disk_number

    @source_image_disk_number.setter
    def source_image_disk_number(self, value):
        self._source_image_disk_number = value

    @property
    def image_disk_allocation_type(self):
        return self._image_disk_allocation_type

    @image_disk_allocation_type.setter
    def image_disk_allocation_type(self, value):
        self._image_disk_allocation_type = value

    @property
    def allocation_area_name_or_volser(self):
        return self._allocation_area_name_or_volser

    @allocation_area_name_or_volser.setter
    def allocation_area_name_or_volser(self, value):
        self._allocation_area_name_or_volser = value

    @property
    def image_disk_mode(self):
        return self._image_disk_mode

    @image_disk_mode.setter
    def image_disk_mode(self, value):
        self._image_disk_mode = value

    @property
    def read_password(self):
        return self._read_password

    @read_password.setter
    def read_password(self, value):
        self._read_password = value

    @property
    def write_password(self):
        return self._write_password

    @write_password.setter
    def write_password(self, value):
        self._write_password = value

    @property
    def multi_password(self):
        return self._multi_password

    @multi_password.setter
    def multi_password(self, value):
        self._multi_password = value

    @property
    def operation_id(self):
        return self._operation_id

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = value

    def pack(self, **kwargs):
        idn_len = len(self._image_disk_number)
        sin_len = len(self._source_image_name)
        sidn_len = len(self._source_image_disk_number)
        idat_len = len(self._image_disk_allocation_type)
        aanov_len = len(self._allocation_area_name_or_volser)
        idm_len = len(self._image_disk_mode)
        rp_len = len(self._read_password)
        wp_len = len(self._write_password)
        mp_len = len(self._multi_password)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        # source_image_name_length (int4)
        # source_image_name (string,1-8,char42)
        # source_image_disk_number_length (int4)
        # source_image_disk_number (string,1-4,char16)
        # image_disk_allocation_type_length (int4)
        # image_disk_allocation_type (string,0-10,char10)
        #                            (string,5,AUTOG)
        #                            (string,5,AUTOR)
        #                            (string,5,AUTOV)
        #                            (string,5,DEVNO)
        # allocation_area_name_or_volser_length (int4)
        # allocation_area_name_or_volser (string,0-8,char42)
        #                                (string,0-6,char42)
        #                                (string,0-4,char42)
        # image_disk_mode_length (int4)
        # image_disk_mode (string,0-5,char26)
        # read_password_length (int4)
        # read_password (string,0-8,charNB)
        # write_password_length (int4)
        # write_password (string,0-8,charNB)
        # multi_password_length (int4)
        # multi_password (string,0-8,charNB)
        fmt = "!I%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%ds" % \
            (idn_len,
             sin_len,
             sidn_len,
             idat_len,
             aanov_len,
             idm_len,
             rp_len,
             wp_len,
             mp_len)

        buf = struct.pack(fmt,
                          idn_len,
                          bytes(self._image_disk_number, "UTF-8"),
                          sin_len,
                          bytes(self._source_image_name, "UTF-8"),
                          sidn_len,
                          bytes(self._source_image_disk_number, "UTF-8"),
                          idat_len,
                          bytes(self._image_disk_allocation_type, "UTF-8"),
                          aanov_len,
                          bytes(self._allocation_area_name_or_volser, "UTF-8"),
                          idm_len,
                          bytes(self._image_disk_mode, "UTF-8"),
                          rp_len,
                          bytes(self._read_password, "UTF-8"),
                          wp_len,
                          bytes(self._write_password, "UTF-8"),
                          mp_len,
                          bytes(self._multi_password, "UTF-8"))
 
        return buf

    def unpack(self, buf):
        offset = 0

        # operation_id (int4; range -1-2147483647)
        self._operation_id, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

