
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

class Image_Disk_Create_DM(Request):
    # Allocation unit size
    CYLINDERS = 1
    BLK0512 = 2
    BLK1024 = 3
    BLK2048 = 4
    BLK4096 = 5
    allocation_unit_size_names = {CYLINDERS: "CYLINDERS", BLK0512: "BLK0512", BLK1024: "BLK1024", BLK2048: "BLK2048", BLK4096: "BLK4096"}

    # Image disk formatting
    UNSPECIFIED = 0
    NONE = 1
    CMS0512 = 2
    CMS1024 = 3
    CMS2048 = 4
    CMS4096 = 5
    CMS = 6

    image_disk_formatting_names = {UNSPECIFIED: "UNSPECIFIED", NONE: "NONE", CMS0512: "CMS0512", CMS1024: "CMS1024", CMS2048: "CMS2048", CMS4096: "CMS4096", CMS: "CMS"}

    def __init__(self,
                 image_disk_number = "",
                 image_disk_device_type = "",
                 image_disk_allocation_type = "",
                 allocation_area_name_or_volser = "",
                 allocation_unit_size = 0,
                 image_disk_size = 0,
                 image_disk_mode = "",
                 image_disk_formatting = UNSPECIFIED,
                 image_disk_label = "",
                 read_password = "",
                 write_password = "",
                 multi_password = "",
                 **kwargs):
        super(Image_Disk_Create_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_disk_number = image_disk_number
        self._image_disk_device_type = image_disk_device_type
        self._image_disk_allocation_type = image_disk_allocation_type
        self._allocation_area_name_or_volser = allocation_area_name_or_volser
        self._allocation_unit_size = allocation_unit_size
        self._image_disk_size = image_disk_size
        self._image_disk_mode = image_disk_mode
        self._image_disk_formatting = image_disk_formatting
        self._image_disk_label = image_disk_label
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
    def image_disk_device_type(self):
        return self._image_disk_device_type

    @image_disk_device_type.setter
    def image_disk_device_type(self, value):
        self._image_disk_device_type = value

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
    def allocation_unit_size(self):
        return self._allocation_unit_size

    @allocation_unit_size.setter
    def allocation_unit_size(self, value):
        self._allocation_unit_size = value

    @property
    def image_disk_size(self):
        return self._image_disk_size

    @image_disk_size.setter
    def image_disk_size(self, value):
        self._image_disk_size = value

    @property
    def image_disk_mode(self):
        return self._image_disk_mode

    @image_disk_mode.setter
    def image_disk_mode(self, value):
        self._image_disk_mode = value

    @property
    def image_disk_formatting(self):
        return self._image_disk_formatting

    @image_disk_formatting.setter
    def image_disk_formatting(self, value):
        self._image_disk_formatting = value

    @property
    def image_disk_label(self):
        return self._image_disk_label

    @image_disk_label.setter
    def image_disk_label(self, value):
        self._image_disk_label = value

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

    def pack(self):
        idn_len = len(self._image_disk_number)
        iddt_len = len(self._image_disk_device_type)
        idat_len = len(self._image_disk_allocation_type)
        aanov_len = len(self._allocation_area_name_or_volser)
        idm_len = len(self._image_disk_mode)
        idl_len = len(self._image_disk_label)
        rp_len = len(self._read_password)
        wp_len = len(self._write_password)
        mp_len = len(self._multi_password)

        # image_disk_number_length (int4)
        # image_disk_number (string,1-4,char16)
        # image_disk_device_type_length (int4)
        # image_disk_device_type (string,1-8,char37)
        # image_disk_allocation_type_length (int4)
        # image_disk_allocation_type (string,0-10,char10)
        #                            (string,5,AUTOG)
        #                            (string,5,AUTOR)
        #                            (string,5,AUTOV)
        #                            (string,5,DEVNO)
        #                            (string,6,T-DISK)
        #                            (string,6,V-DISK)
        # allocation_area_name_or_volser_length (int4)
        # allocation_area_name_or_volser (string,1-8,char42)
        #                                (string,1-6,char42)
        #                                (string,4-4,char42)
        # allocation_unit_size (int1)
        # image_disk_size (int4; range 0-2147483640)
        # image_disk_mode_length (int4)
        # image_disk_mode (string,1-5,char26)
        # image_disk_formatting (int1)
        # image_disk_label_length (int4)
        # image_disk_label (string,0-6,charNB)
        # read_password_length (int4)
        # read_password (string,0-8,charNB)
        # write_password_length (int4)
        # write_password (string,0-8,charNB)
        # multi_password_length (int4)
        # multi_password (string,0-8,charNB)
        fmt = "!I%dsI%dsI%dsI%dsBII%dsBI%dsI%dsI%dsI%ds" % \
            (idn_len,
             iddt_len,
             idat_len,
             aanov_len,
             idm_len,
             idl_len,
             rp_len,
             wp_len,
             mp_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_disk_number),
                          iddt_len,
                          s2b(self._image_disk_device_type),
                          idat_len,
                          s2b(self._image_disk_allocation_type),
                          aanov_len,
                          s2b(self._allocation_area_name_or_volser),
                          self._allocation_unit_size,
                          self._image_disk_size,
                          idm_len,
                          s2b(self._image_disk_mode),
                          self._image_disk_formatting,
                          idl_len,
                          s2b(self._image_disk_label),
                          rp_len,
                          s2b(self._read_password),
                          wp_len,
                          s2b(self._write_password),
                          mp_len,
                          s2b(self._multi_password))
 
        return buf

    def unpack(self, buf):
        # operation_id (int4; range -1-2147483647)
        self._operation_id, = struct.unpack("!I", buf)

