
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

class Shared_Memory_Access_Remove_DM(Request):
    def __init__(self,
                 memory_segment_name = "",
                 **kwargs):
        super(Shared_Memory_Access_Remove_DM, self).__init__(**kwargs)

        # Request parameters
        self._memory_segment_name = memory_segment_name

    @property
    def memory_segment_name(self):
        return self._memory_segment_name

    @memory_segment_name.setter
    def memory_segment_name(self, value):
        self._memory_segment_name = value

    def pack(self):
        msn_len = len(self._memory_segment_name)

        # memory_segment_name_length (int4)
        # memory_segment_name (string,1-8,char42)
        fmt = "!I%ds" % (msn_len)

        buf = struct.pack(fmt,
                          msn_len,
                          s2b(self._memory_segment_name))

        return buf
