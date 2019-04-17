
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

class Metadata_Set(Request):
    def __init__(self,
                 metadata_entry_array = [],
                 **kwargs):
        super(Metadata_Set, self).__init__(**kwargs)

        # Request parameters
        self._metadata_entry_array = metadata_entry_array

    @property
    def metadata_entry_array(self):
        return self._metadata_entry_array

    @metadata_entry_array.setter
    def metadata_entry_array(self, value):
        self._metadata_entry_array = value

    def pack(self):
        buf = b""

        for metadata_entry_name, metadata in self._metadata_entry_array:
            men_len = len(metadata_entry_name)
            m_len = len(metadata)

            # metadata_entry_name_length (int4)
            # metadata_entry_name (string,1-1024,charNB)
            # metadata_length (int4)
            # metadata (string,1-maxlength,charNA)
            fmt = "!I%dsI%ds" % (men_len, m_len)

            entry = struct.pack(fmt,
                                men_len,
                                s2b(metadata_entry_name),
                                m_len,
                                s2b(metadata))

            # metadata_entry_structure_length (int4)
            buf += struct.pack("!I", len(entry)) + entry

        # metadata_entry_array_length (int4)
        # metadata_entry_array (array)
        buf = struct.pack("!I", len(buf)) + buf

        return buf
