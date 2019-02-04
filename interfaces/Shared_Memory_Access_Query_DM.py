
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

class Shared_Memory_Access_Query_DM(Smapi_Request_Base):
    def __init__(self,
                 memory_segment_name = b"",
                 **kwargs):
        super(Shared_Memory_Access_Query_DM, self). \
            __init__(b"Shared_Memory_Access_Query_DM", **kwargs)

        # Request parameters
        self._memory_segment_name = memory_segment_name

        # Response values
        self._name_array = []

    @property
    def memory_segment_name(self):
        return self._memory_segment_name

    @memory_segment_name.setter
    def memory_segment_name(self, value):
        self._memory_segment_name = value

    @property
    def name_array(self):
        return self._name_array

    @name_array.setter
    def name_array(self, value):
        self._name_array = value

    def pack(self):
        msn_len = len(self._memory_segment_name)

        # memory_segment_name_length (int4)
        # memory_segment_name (string,1-8,char42)
        fmt = b"!I%ds" % (msn_len)

        buf = struct.pack(fmt,
                          msn_len,
                          self._memory_segment_name)

        return super(Shared_Memory_Access_Query_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Shared_Memory_Access_Query_DM, self).unpack(buf, offset)

        # spool_information_structure_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4
        
        self._name_array = []
        while alen > 0:
            entry = Obj()
            self._name_array.append(entry)

            # name_length (int4)
            nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # name (string,1-8,char42)
            entry.name = buf[offset:offset + nlen]
            offset += nlen

            alen -= (nlen + 4)

        return offset

