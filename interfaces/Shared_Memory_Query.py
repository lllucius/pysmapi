
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

class Shared_Memory_Query(Request):

    # Memory segment status
    SKELETON = 1
    NONRESTRICTED = 2
    RESTRICTED = 3
    PENDINGPURGE = 4
    memory_segment_status_names = ["PENDINGPURGE"]

    # Page access descriptor
    SW = 1
    EW = 2
    SR = 3
    ER = 4
    SN = 5
    EN = 6
    SC = 7
    page_access_descriptor_names = ["SC"]

    def __init__(self,
                 memory_segment_name = 0,
                 **kwargs):
        super(Shared_Memory_Query, self).__init__(**kwargs)

        # Request parameters
        self._memory_segment_name = memory_segment_name

        # Response values
        self._memory_segment_array = []

    @property
    def memory_segment_name(self):
        return self._memory_segment_name

    @memory_segment_name.setter
    def memory_segment_name(self, value):
        self._memory_segment_name = value

    @property
    def memory_segment_array(self):
        return self._memory_segment_array

    @memory_segment_array.setter
    def memory_segment_array(self, value):
        self._memory_segment_array = value

    def pack(self):
        msn_len = len(self._memory_segment_name)

        # memory_segment_name_length (int4)
        # memory_segment_name (string,1-8,char42)
        fmt = "!I%ds" % (msn_len)
  
        buf = struct.pack(fmt,
                          msn_len,
                          bytes(self._memory_segment_name, "UTF-8"))

        return buf

    def unpack(self, buf):
        offset = 0

        # memory_segment_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._memory_segment_array = []
        while alen > 0:
            entry = Obj()
            self._memory_segment_array.append(entry)

            # memory_segment_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # memory_segment_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # memory_segment_name (string,1-8,char42)
            entry.userid = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen

            # memory_segment_status (int1)
            entry.memory_segment_status = ord(buf[offset])
            offset += 1

            # page_range_array_length (int4)
            pralen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            entry.page_range_array = []
            while pralen > 0:
                praent = Obj()
                entry.page_range_array.append(praent)

                # page_range_structure_length (int4)
                prslen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4
                pralen -= (prslen + 4)

                # begin_page (int8; range 0-524031)
                # end_page (int8; range 0-524031)
                # page_access_descriptor (int1)
                praent.begin_page, \
                praent.end_page, \
                praent.page_access_descriptor = struct.unpack("!QQB", buf[offset:offset + prslen])
                offset += prslen

