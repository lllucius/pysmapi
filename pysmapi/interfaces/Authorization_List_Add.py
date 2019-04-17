
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

class Authorization_List_Add(Request):
    def __init__(self,
                 for_id = "=",
                 function_id = "",
                 **kwargs):
        super(Authorization_List_Add, self).__init__(**kwargs)

        # Request paramters
        self._for_id = for_id
        self._function_id = function_id

    @property
    def for_id(self):
        return self._for_id

    @for_id.setter
    def for_id(self, value):
        self._for_id = value

    @property
    def function_id(self):
        return self._function_id

    @function_id.setter
    def function_id(self, value):
        self._function_id = value

    def pack(self):
        for_len = len(self._for_id)
        func_len = len(self.function_id)

        # for_id_length (int4)
        # for_id (string,1-8,char42)
        #        (string,1-64,char43)
        #        (string,1,=)
        #        (string,3,ALL)
        # function_id_length (int4)
        # function_id (string,1-64,char43)
        #             (string,3,ALL)
        fmt = "!I%dsI%ds" % (for_len, func_len)
        buf = struct.pack(fmt,
                          for_len,
                          s2b(self._for_id),
                          func_len,
                          s2b(self._function_id))
 
        return buf

