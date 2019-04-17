
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

class Metadata_Get(Request):
    def __init__(self,
                 metadata_name_list = "",
                 **kwargs):
        super(Metadata_Get, self).__init__(**kwargs)

        # Request parameters
        self._metadata_name_list = metadata_name_list

        # Response values
        self._metadata_entry_array = []

    @property
    def metadata_name_list(self):
        return self._metadata_name_list

    @metadata_name_list.setter
    def metadata_name_list(self, value):
        self._metadata_name_list = value

    @property
    def metadata_entry_array(self):
        return self._metadata_entry_array

    @metadata_entry_array.setter
    def metadata_entry_array(self, value):
        self._metadata_entry_array = value

    def pack(self):
        # id=value (string,1-8,char42) (ASCIIZ)
        buf = "%s\x00" % (self._metadata_name_list)

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # metadata_entry_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._metadata_entry_array = []
        while alen > 0:
            entry = Obj()
            self._metadata_entry_array.append(entry)

            # CPU_info_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # metadata_entry_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # metadata_entry_name (string,1-1024,charNB)
            entry.metadata_entry_name = b2s(buf[offset:offset + nlen])
            offset += nlen

            # metadata_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # metadata (string,1-maxlength,charNA)
            entry.metadata = b2s(buf[offset:offset + nlen])
            offset += nlen

