
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

class Virtual_Network_Vswitch_Delete_Extended(Request):
    def __init__(self,
                 switch_name = "",
                 persist = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Delete_Extended, self).__init__(**kwargs)

        # Request parameters
        self._switch_name = switch_name
        self._persist = persist

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def persist(self):
        return self._persist

    @persist.setter
    def persist(self, value):
        self._persist = value

    def pack(self):
        buf = ""

        # switch_name (string,1-8,char36 plus @#$_)
        buf += f"switch_name={self._switch_name}\x00"

        # persist=value (string,0-3,char42)
        buf += f"persist={self._persist}\x00"

        return s2b(buf)

