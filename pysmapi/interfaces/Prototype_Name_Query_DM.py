
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

class Prototype_Name_Query_DM(Request):
    def __init__(self,
                 **kwargs):
        super(Prototype_Name_Query_DM, self).__init__(**kwargs)

        # Response values
        self._prototype_name_array = []

    @property
    def prototype_name_array(self):
        return self._prototype_name_array

    @prototype_name_array.setter
    def prototype_name_array(self, value):
        self._prototype_name_array = value

    def unpack(self, buf):
        offset = 0

        # prototype_name_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # prototype_name_array
        while alen > 0:
            entry = Obj()
            self._prototype_name_array.append(entry)

            # prototype_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # prototype_name (string,1-8,char42)
            entry.prototype_name = b2s(buf[offset:offset + nlen])
            offset += nlen

            alen -= (nlen + 4)

