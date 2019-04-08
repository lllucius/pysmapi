
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

class Shared_Memory_Replace(Request):
    def __init__(self,
                 memory_segment_name = 0,
                 memory_access_identifier = "",
                 **kwargs):
        super(Shared_Memory_Replace, self).__init__(**kwargs)

        # Request parameters
        self._memory_segment_name = memory_segment_name
        self._memory_access_identifier = memory_access_identifier

    @property
    def memory_segment_name(self):
        return self._memory_segment_name

    @memory_segment_name.setter
    def memory_segment_name(self, value):
        self._memory_segment_name = value

    @property
    def memory_access_identifier(self):
        return self._memory_access_identifier

    @memory_access_identifier.setter
    def memory_access_identifier(self, value):
        self._memory_access_identifier = value

    def pack(self):
        msn_len = len(self._memory_segment_name)
        mai_len = len(self._memory_access_identifier)

        # memory_segment_name_length (int4)
        # memory_segment_name (string,1-8,char42)
        # memory_access_identifier_length (int4)
        # memory_access_identifier (string,0-8,char42)
        fmt = "!I%dsI%ds" % \
            (msn_len,
             mai_len)
  
        buf = struct.pack(fmt,
                          msn_len,
                          bytes(self._memory_segment_name, "UTF-8"),
                          mai_len,
                          bytes(self._memory_access_identifier, "UTF-8"))

        return buf
