
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

class Query_ABEND_Dump(Smapi_Request_Base):

    # Abend dump loc
    READER = 1
    SFS = 2
    abend_dump_loc_names = ["?", "READER", "SFS DIRECTORY"]

    def __init__(self,
                 location = b"",
                 **kwargs):
        super(Query_ABEND_Dump, self). \
            __init__(b"Query_ABEND_Dump", **kwargs)

        # Request parameters
        self._location = location

        # Response values
        self._abend_dump_array = []

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def abend_dump_array(self):
        return self._abend_dump_array

    @abend_dump_array.setter
    def abend_dump_array(self, value):
        self._abend_dump_array = value

    def pack(self):
        # id=value (string,1-8,char42) (ASCIIZ)
        buf = b"location=%s\x00" % (self._location)

        return super(Query_ABEND_Dump, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Query_ABEND_Dump, self).unpack(buf, offset)

        # abend_dump_array_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        self._abend_dump_array = []
        while alen > 0:
            entry = Obj()
            self._abend_dump_array.append(entry)

            # abend_dump_loc (int1)
            # abend_dump_id (string,8,char42)
            # abend_dump_date (string,10,char42)
            # abend_dump_dist (string,8,char42 plus blank)
            fmt = b"!B8s10s8s"
            size = struct.calcsize(fmt)

            entry.abend_dump_loc,
            entry.abend_dump_id,
            entry.abend_dump_date,
            entry.abend_dump_dist = struct.unpack(fmt, buf[offset:offset + size])
            offset += size
            alen -= size

        return offset


