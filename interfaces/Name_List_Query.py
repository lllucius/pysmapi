
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

class Name_List_Query(Request):
    def __init__(self,
                 **kwargs):
        super(Name_List_Query, self).__init__(**kwargs)

        # Response Values
        self._name_array = []

    @property
    def name_array(self):
        return self._name_array

    @name_array.setter
    def name_array(self, value):
        self._name_array = value

    def unpack(self, buf):
        offset = 0

        # name_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._name_array = []
        while alen > 0:
            entry = Obj()
            self._name_array.append(entry)

            # name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= 4

            # name (string,1-8,char42)
            #      (string,1-64,char43)
            entry.name = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen
            alen -= nlen

