
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

class Image_Volume_Space_Define_Extended_DM(Request):

    # Function type
    FT_1 = 1
    FT_2 = 2
    FT_3 = 3
    FT_4 = 4
    FT_5 = 5
    function_type_names = ["FT_5"]

    # Device type
    DT_UNSPECIFIED = 0
    DT_3390 = 1
    DT_9336 = 2
    DT_3380 = 3
    DT_FB_512 = 4
    device_type_names = ["FB-512"]

    # Alloc method
    AM_0 = 0
    AM_1 = 1
    AM_2 = 2
    alloc_method_names = ["AM_2"]

    def __init__(self,
                 function_type = 0,
                 region_name = "",
                 image_vol_id = "",
                 start_cylinder = 0,
                 size = 0,
                 group_name = "",
                 device_type = 0,
                 alloc_method = 0,
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
        buf += "function_type=%s\x00" % (str(self._function_type).encode())

        # region_name (string,1-4,char16)
        buf += "region_name=%s\x00" % (self._region_name)

        # image_vol_id (string,1-6,char42)
        buf += "image_vol_id=%s\x00" % (self._image_vol_id)

        # start_cylinder (int4; range 0-2147483640)
        buf += "start_cylinder=%s\x00" % (str(self._start_cylinder).encode())

        # size (int4; range 1-2147483640)
        buf += "size=%s\x00" % (str(self._size).encode())

        # group_name (string,0-8,char42)
        buf += "group_name=%s\x00" % (self._group_name)

        # device_type (int1)
        buf += "device_type=%s\x00" % (str(self._device_type).encode())

        # alloc_method (int1)
        buf += "alloc_method=%s\x00" % (str(self._alloc_method).encode())

        # image_volume_space_define_names_length (int4)
        buf = struct.pack("!I", len(buf)) + bytes(buf, "UTF-8")

        return buf