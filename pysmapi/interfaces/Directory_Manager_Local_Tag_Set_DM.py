
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

class Directory_Manager_Local_Tag_Set_DM(Request):
    def __init__(self,
                 tag_name = "",
                 tag_value = 0,
                 **kwargs):
        super(Directory_Manager_Local_Tag_Set_DM, self).__init__(**kwargs)

        # Request parameters
        self._tag_name = tag_name
        self._tag_value = tag_value

    @property
    def tag_name(self):
        return self._tag_name

    @tag_name.setter
    def tag_name(self, value):
        self._tag_name = value

    @property
    def tag_value(self):
        return self._tag_value

    @tag_value.setter
    def tag_value(self, value):
        self._tag_value = value

    def pack(self):
        tn_len = len(self._tag_name)
        tv_len = len(self._tag_value)

        # tag_name_length (int4)
        # tag_name (string,1-8,char36)
        # tag_value_length (int4)
        # tag_value (string,1-1024,charNA)
        fmt = "!I%dsI%ds" % (tn_len, tv_len)
        buf = struct.pack(fmt,
                          tn_len,
                          s2b(self._tag_name),
                          tv_len,
                          s2b(self._tag_value))

        return buf
