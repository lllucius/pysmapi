
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

class Name_List_Remove(Request):
    def __init__(self,
                 name = "",
                 **kwargs):
        super(Name_List_Remove, self).__init__(**kwargs)

        # Request parameters
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def pack(self):
        n_len = len(self._name)

        # name_length (int4)
        # name (string,1-8,char42)
        #      (string,1-64,char43)
        fmt = "!I%ds" % (n_len)
        buf = struct.pack(fmt,
                          n_len,
                          bytes(self._name, "UTF-8"))

        return buf
