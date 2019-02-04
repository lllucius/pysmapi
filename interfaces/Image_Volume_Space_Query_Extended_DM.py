
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

class Image_Volume_Space_Query_Extended_DM(Smapi_Request_Base):

    # Query type
    DEFINITION = 1
    FREE = 2
    USED = 3
    query_type_names = ["?", "DEFINITION", "FREE", "USED"]

    # Entry type
    VOLUME = 1
    REGION = 2
    GROUP = 3
    entry_type_names = ["?", "VOLUME", "REGION", "GROUP"]
    
    def __init__(self,
                 query_type = 0,
                 entry_type = b"",
                 entry_names = b"",
                 **kwargs):
        super(Image_Volume_Space_Query_Extended_DM, self). \
            __init__(b"Image_Volume_Space_Query_Extended_DM", **kwargs)

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

    def pack(self):
        buf = b""

        # query_type=value (string,1,char10)
        buf += b"query_type=%s\x00" % (self._query_type)

        # entry_type=value (string,1,char10)
        buf += b"entry_type=%s\x00" % (self._entry_type)

        # entry_names=value (string,0-255,char42 plus blank)
        buf += b"entry_names=%s\x00" % (self._entry_names)

        # image_volume_space_query_names_length (int4)
        buf = struct.pack(b"!I", len(buf)) + buf

        return super(Image_Volume_Space_Query_Extended_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Image_Volume_Space_Query_Extended_DM, self).unpack(buf, offset)

        self._record_array = buf[offset:-1].split(b"\x00")
        offset += len(buf)

        return offset

