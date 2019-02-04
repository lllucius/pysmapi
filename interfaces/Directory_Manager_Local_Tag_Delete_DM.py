
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

class Directory_Manager_Local_Tag_Delete_DM(Smapi_Request_Base):
    def __init__(self,
                 tag_name = b"",
                 **kwargs):
        super(Directory_Manager_Local_Tag_Delete_DM, self). \
            __init__(b"Directory_Manager_Local_Tag_Delete_DM", **kwargs)

        # Request parameters
        self._tag_name = tag_name

    @property
    def tag_name(self):
        return self._tag_name

    @tag_name.setter
    def tag_name(self, value):
        self._tag_name = value

    def pack(self):
        tn_len = len(self._tag_name)

        # tag_name_length (int4)
        # tag_name (string,1-8,char36)
        fmt = b"!I%ds" % (tn_len)
        buf = struct.pack(fmt,
                          tn_len,
                          self._tag_name)

        return super(Directory_Manager_Local_Tag_Delete_DM, self).pack(buf)

