
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

from base import Smapi_Request_Base, Obj

class Image_Disk_Copy_DM(Smapi_Request_Base):

    # Allocation unit size
    CYLINDERS = 1
    BLK0512 = 2
    BLK1024 = 3
    BLK2048 = 4
    BLK4096 = 5
    source_image_disk_number_names = ["?", "CYLINDERS", "BLK0512", "BLK1024", "BLK2048", "BLK4096"]

    # Image disk formatting
    UNSPECIFIED = 0
    NONE = 1
    CMS0512 = 2
    CMS1024 = 3
    CMS2048 = 4
    CMS4096 = 5
    CMS = 6
    image_disk_formatting_names = ["UNSPECIFIED", "NONE", "CMS0512", "CMS1024", "CMS2048", "CMS4096", "CMS"]

    def __init__(self,
                 image_disk_number = b"",
                 source_image_name = b"",
                 source_image_disk_number = b"",
                 image_disk_allocation_type = b"",
                 allocation_area_name_or_volser = b"",
                 image_disk_mode = b"",
                 read_password = b"",
                 write_password = b"",
                 multi_password = b"",
                 **kwargs):
        super(Image_Disk_Copy_DM, self). \
            __init__(b"Image_Disk_Copy_DM", **kwargs)

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


    def pack(self):
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
        # source_image_disk_number (int1)
        # image_disk_mode_length (int4)
        # image_disk_mode (string,0-5,char26)
        # read_password_length (int4)
        # read_password (string,0-8,charNB)
        # write_password_length (int4)
        # write_password (string,0-8,charNB)
        # multi_password_length (int4)
        # multi_password (string,0-8,charNB)
        fmt = b"!I%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%ds" % \
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
                          self._image_disk_number,
                          sin_len,
                          self._source_image_name,
                          sidn_len,
                          self._source_image_disk_number,
                          idat_len,
                          self._image_disk_allocation_type,
                          aanov_len,
                          self._allocation_area_name_or_volser,
                          idm_len,
                          self._image_disk_mode,
                          rp_len,
                          self._read_password,
                          wp_len,
                          self._write_password,
                          mp_len,
                          self._multi_password)
 
        return super(Image_Disk_Copy_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Image_Disk_Copy_DM, self).unpack(buf, offset)

        # operation_id (int4; range -1-2147483647)
        self._operation_id, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        return offset

