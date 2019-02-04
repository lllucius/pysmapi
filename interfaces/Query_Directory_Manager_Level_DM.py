
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

class Query_Directory_Manager_Level_DM(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(Query_Directory_Manager_Level_DM, self). \
            __init__(b"Query_Directory_Manager_Level_DM", **kwargs)

        # Response Values
        self._directory_manager_level = []

    @property
    def directory_manager_level(self):
        return self._directory_manager_level

    @directory_manager_level.setter
    def directory_manager_level(self, value):
        self._directory_manager_level = value

    def unpack(self, buf, offset):
        offset = super(Query_Directory_Manager_Level_DM, self).unpack(buf, offset)

        # directory_manager_level_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # directory_manager_level (string,1-100,charNA)
        self._directory_manager_level = buf[offset:offset + nlen]
        offset += nlen

        return offset

