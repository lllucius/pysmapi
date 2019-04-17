
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

class Query_ABEND_Dump(Request):
    # Abend dump loc
    READER = 1
    SFS = 2
    abend_dump_loc_names = {READER: "READER", SFS: "SFS"}

    def __init__(self,
                 location = "",
                 **kwargs):
        super(Query_ABEND_Dump, self).__init__(**kwargs)

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
        buf = "location=%s\x00" % (self._location)

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        self._abend_dump_array = []
        while offset < len(buf):
            entry = Obj()
            self._abend_dump_array.append(entry)

            # abend_dump_loc (int1)
            entry.abend_dump_loc = buf[offset]
            offset += 1

            # abend_dump_id (string,8,char42)
            entry.abend_dump_id = b2s(buf[offset:offset + 8]).strip()
            offset += 8

            # abend_dump_date (string,10,char42)
            entry.abend_dump_date = b2s(buf[offset:offset + 10]).strip()
            offset += 10

            # abend_dump_dist (string,8,char42 plus blank)
            entry.abend_dump_dist = b2s(buf[offset:offset + 8]).strip()
            offset += 8

