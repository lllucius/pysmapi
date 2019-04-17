
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

class Image_Volume_Space_Remove_DM(Request):
    # Function type
    FT_1 = 1
    FT_2 = 2
    FT_3 = 3
    FT_4 = 4
    FT_5 = 5
    FT_6 = 6
    FT_7 = 7
    function_type_names = {FT_1: "1", FT_2: "2", FT_3: "3", FT_4: "4", FT_5: "5", FT_6: "6", FT_7: "7"}

    def __init__(self,
                 function_type = 0,
                 region_name = "",
                 image_vol_id = "",
                 group_name = "",
                 **kwargs):
        super(Image_Volume_Space_Remove_DM, self).__init__(**kwargs)

        # Request parameters
        self._function_type = function_type
        self._region_name = region_name
        self._image_vol_id = image_vol_id
        self._group_name = group_name

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
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    def pack(self):
        rn_len = len(self._region_name)
        ivi_len = len(self._image_vol_id)
        gn_len = len(self._group_name)

        # function_type (int1)
        # region_name_length (int4)
        # region_name (string,1-4,char16)
        # image_vol_id_length (int4)
        # image_vol_id (string,1-6,char42)
        # group_name_length (int4)
        # group_name (string,0-8,char42)
        fmt = "!BI%dsI%dsI%ds" % \
            (rn_len,
             ivi_len,
             gn_len)
  
        buf = struct.pack(fmt,
                          self._function_type,
                          rn_len,
                          s2b(self._region_name),
                          ivi_len,
                          s2b(self._image_vol_id),
                          gn_len,
                          s2b(self._group_name))

        return buf
