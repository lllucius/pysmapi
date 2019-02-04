
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

class Metadata_Delete(Smapi_Request_Base):
    def __init__(self,
                 metadata_name_list = b"",
                 **kwargs):
        super(Metadata_Delete, self). \
            __init__(b"Metadata_Delete", **kwargs)

        # Request parameters
        self._metadata_name_list = metadata_name_list

    @property
    def metadata_name_list(self):
        return self._metadata_name_list

    @metadata_name_list.setter
    def metadata_name_list(self, value):
        self._metadata_name_list = value

    def pack(self):
        # id=value (string,1-8,char42) (ASCIIZ)
        buf = b"%s\x00" % (self._metadata_name_list)

        return super(Metadata_Delete, self).pack(buf)

