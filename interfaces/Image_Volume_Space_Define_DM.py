
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

class Image_Volume_Space_Define_DM(Smapi_Request_Base):

    # Function type
    FT_1 = 1
    FT_2 = 2
    FT_3 = 3
    FT_4 = 4
    FT_5 = 5
    function_type_names = ["?", "FT_1", "FT_2", "FT_3", "FT_4", "FT_5"]

    # Device type
    DT_UNSPECIFIED = 0
    DT_3390 = 1
    DT_9336 = 2
    DT_3380 = 3
    DT_FB_512 = 4
    device_type_names = ["UNSPECIFIED", "3390", "9336", "3380", "FB-512"]
    
    def __init__(self,
                 function_type = 0,
                 region_name = b"",
                 image_vol_id = b"",
                 start_cylinder = 0,
                 size = 0,
                 group_name = b"",
                 device_type = 0,
                 **kwargs):
        super(Image_Volume_Space_Define_DM, self). \
            __init__(b"Image_Volume_Space_Define_DM", **kwargs)

        # Request parameters
        self._function_type = function_type
        self._region_name = region_name
        self._image_vol_id = image_vol_id
        self._start_cylinder = start_cylinder
        self._size = size
        self._group_name = group_name
        self._device_type = device_type

    @property
    def function_type(self):
        return self._function_type

    @function_type.setter
    def function_type(self, value):
        self._function_type = value

    @property
    def region_name(self):
        return self._region_name

    @region_name.setter
    def region_name(self, value):
        self._region_name = value

    @property
    def image_vol_id(self):
        return self._image_vol_id

    @image_vol_id.setter
    def image_vol_id(self, value):
        self._image_vol_id = value

    @property
    def start_cylinder(self):
        return self._start_cylinder

    @start_cylinder.setter
    def start_cylinder(self, value):
        self._start_cylinder = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        self._device_type = value

    def pack(self):
        rn_len = len(self._region_name)
        ivi_len = len(self._image_vol_id)
        gn_len = len(self._group_name)

        # function_type (int1)
        # region_name_length (int4)
        # region_name (string,1-4,char16)
        # image_vol_id_length (int4)
        # image_vol_id (string,1-6,char42)
        # start_cylinder (int4; range 0-2147483640)
        # size (int4; range 1-2147483640)
        # group_name_length (int4)
        # group_name (string,0-8,char42)
        # device_type (int1)
        fmt = b"!BI%dsI%dsIII%dsB" % \
            (rn_len,
             ivi_len,
             gn_len)
  
        buf = struct.pack(fmt,
                          self._function_type,
                          rn_len,
                          self._region_name,
                          ivi_len,
                          self._image_vol_id,
                          self._start_cylinder,
                          self._size,
                          gn_len,
                          self._group_name,
                          self._device_type)

        return super(Image_Volume_Space_Define_DM, self).pack(buf)

