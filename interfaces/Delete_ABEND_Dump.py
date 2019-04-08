
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

from pysmapi.smapi import Request, Obj

class Delete_ABEND_Dump(Request):
    def __init__(self,
                 id = "",
                 **kwargs):
        super(Delete_ABEND_Dump, self).__init__(**kwargs)

        # Request parameters
        self._id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def pack(self):
        # id=value (string,1-8,char42) (ASCIIZ)
        buf = f"id={self._id}\x00"

        return bytes(buf, "UTF-8")

