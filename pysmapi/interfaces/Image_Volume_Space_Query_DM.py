
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

class Image_Volume_Space_Query_DM(Request):
    # Query type
    DEFINITION = 1
    FREE = 2
    USED = 3
    query_type_names = {DEFINITION: "DEFINITION", FREE: "FREE", USED: "USED"} 

    # Entry type
    VOLUME = 1
    REGION = 2
    GROUP = 3
    entry_type_names = {VOLUME: "VOLUME", REGION: "REGION", GROUP: "GROUP"}
    
    def __init__(self,
                 query_type = 0,
                 entry_type = "",
                 entry_names = "",
                 **kwargs):
        super(Image_Volume_Space_Query_DM, self).__init__(**kwargs)

        # Request parameters
        self._query_type = query_type
        self._entry_type = entry_type
        self._entry_names = entry_names

        # Response values
        self._record_array = []

    @property
    def query_type(self):
        return self._query_type

    @query_type.setter
    def query_type(self, value):
        self._query_type = value

    @property
    def entry_type(self):
        return self._entry_type

    @entry_type.setter
    def entry_type(self, value):
        self._entry_type = value

    @property
    def entry_names(self):
        return self._entry_names

    @entry_names.setter
    def entry_names(self, value):
        self._entry_names = value

    @property
    def record_array(self):
        return self._record_array

    @record_array.setter
    def record_array(self, value):
        self._record_array = value

    def pack(self, **kwargs):
        en_len = len(self._entry_names)

        # query_type (int1)
        # entry_type (int1)
        # entry_names_length (int4)
        # entry_names (string,1-6,char42)
        fmt = "!BBI%ds" % (en_len)
  
        buf = struct.pack(fmt,
                          self._query_type,
                          self._entry_type,
                          en_len,
                          s2b(self._entry_names))

        return buf

    def unpack(self, buf):
        offset = 0

        # prototype_record_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # prototype_record_array
        self._record_array = []
        while alen > 0:
            # record_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # record (string,1-*,charNA)
            self._record_array.append(b2s(buf[offset:offset + nlen]))
            offset += nlen

            alen -= (nlen + 4)

