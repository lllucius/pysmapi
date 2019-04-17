
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

class Image_Volume_Space_Define_Extended_DM(Request):
    # Function type
    FT_1 = 1
    FT_2 = 2
    FT_3 = 3
    FT_4 = 4
    FT_5 = 5
    function_type_names = {FT_1: "1", FT_2: "2", FT_3: "3", FT_4: "4", FT_5: "5"}

    # Device type
    DT_UNSPECIFIED = 0
    DT_3390 = 1
    DT_9336 = 2
    DT_3380 = 3
    DT_FB_512 = 4
    device_type_names = {DT_UNSPECIFIED: "UNSPECIFIED", DT_3390: "3390", DT_9336: "9336", DT_3380: "3380", DT_FB_512: "FB_512"}

    # Alloc method
    AM_0 = 0
    AM_1 = 1
    AM_2 = 2
    alloc_method_names = {AM_0: "0", AM_1: "1", AM_2: "2"}

    def __init__(self,
                 function_type = "",
                 region_name = "",
                 image_vol_id = "",
                 start_cylinder = 0,
                 size = 0,
                 group_name = "",
                 device_type = DT_UNSPECIFIED,
                 alloc_method = AM_0,
                 **kwargs):
        super(Image_Volume_Space_Define_Extended_DM, self).__init__(**kwargs)

        # Request parameters
        self._function_type = function_type
        self._region_name = region_name
        self._image_vol_id = image_vol_id
        self._start_cylinder = start_cylinder
        self._size = size
        self._group_name = group_name
        self._device_type = device_type
        self._alloc_method = alloc_method

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

    @property
    def alloc_method(self):
        return self._alloc_method

    @alloc_method.setter
    def alloc_method(self, value):
        self._alloc_method = value

    def pack(self):
        buf = ""

        # function_type (int1)
        if self._function_type:
            buf += f"function_type={self._function_type}\x00"

        # region_name (string,1-4,char16)
        if self._region_name:
            buf += f"region_name={self._region_name}\x00" 

        # image_vol_id (string,1-6,char42)
        if self._image_vol_id:
            buf += f"image_vol_id={self._image_vol_id}\x00" 

        # start_cylinder (int4; range 0-2147483640)
        if self._start_cylinder:
            buf += f"start_cylinder={self._start_cylinder}\x00" 

        # size (int4; range 1-2147483640)
        if self._size:
            buf += f"size={self._size}\x00" 

        # group_name (string,0-8,char42)
        if self._group_name:
            buf += f"group_name={self._group_name}\x00" 

        # device_type (int1)
        if self._device_type:
            buf += f"device_type={self._device_type}\x00" 

        # alloc_method (int1)
        if self._alloc_method:
            buf += f"alloc_method={self._alloc_method}\x00" 

        # image_volume_space_define_names_length (int4)
        buf = struct.pack("!I", len(buf)) + s2b(buf)

        return buf
