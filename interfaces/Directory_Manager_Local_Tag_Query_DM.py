
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

class Directory_Manager_Local_Tag_Query_DM(Smapi_Request_Base):
    def __init__(self,
                 tag_name = b"",
                 **kwargs):
        super(Directory_Manager_Local_Tag_Query_DM, self). \
            __init__(b"Directory_Manager_Local_Tag_Query_DM", **kwargs)

        # Request values
        self._tag_name = tag_name

        # Response values
        self._tag_value = b""

    @property
    def tag_name(self):
        return self._tag_name

    @tag_name.setter
    def tag_name(self, value):
        self._tag_name = value

    @property
    def tag_value(self):
        return self._tag_value

    @tag_value.setter
    def tag_value(self, value):
        self._tag_value = value

    def pack(self):
        tn_len = len(self._tag_name)

        # tag_name_length (int4)
        # tag_name (string,1-8,char36)
        fmt = b"!I%ds" % (tn_len)
        buf = struct.pack(fmt,
                          tn_len,
                          self._tag_name)

        return super(Directory_Manager_Local_Tag_Query_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Directory_Manager_Local_Tag_Query_DM, self).unpack(buf, offset)

        # tag_value_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # tag_value (string,1-1024,charNA)
        self._tag_value = buf[offset:offset + nlen]

        return offset

