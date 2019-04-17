
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

class Directory_Manager_Search_DM(Request):
    def __init__(self,
                 search_pattern = "",
                 **kwargs):
        super(Directory_Manager_Search_DM, self).__init__(**kwargs)

        # Request parameters
        self._search_pattern = search_pattern

        # Response values
        self._statement_array = []

    @property
    def search_pattern(self):
        return self._search_pattern

    @search_pattern.setter
    def search_pattern(self, value):
        self._search_pattern = value

    @property
    def function_id(self):
        return self._function_id

    @function_id.setter
    def function_id(self, value):
        self._function_id = value

    @property
    def statement_array(self):
        return self._statement_array

    @statement_array.setter
    def statement_array(self, value):
        self._statement_array = value

    def pack(self):
        sp_len = len(self._search_pattern)

        # search_pattern_length (int4)
        # search_pattern (string,1-72,charNA)
        fmt = "!I%ds" % (sp_len)
        buf = struct.pack(fmt,
                          sp_len,
                          s2b(self._search_pattern))
 
        return buf
        
    def unpack(self, buf):
        offset = 0

        # statement_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._statement_array = []
        while alen > 0:
            entry = Obj()
            self._statement_array.append(entry)

            # target_id_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= 4

            # target_id (string,1-8,char42)
            entry.target_id = b2s(buf[offset:offset + nlen])
            offset += nlen
            alen -= nlen

            # statement_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= 4

            # statement (string,1-72,charNA)
            entry.statement = b2s(buf[offset:offset + nlen])
            offset += nlen
            alen -= nlen

