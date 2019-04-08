
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

class Virtual_Network_LAN_Delete(Request):
    def __init__(self,
                 lan_name = "",
                 lan_owner = "",
                 **kwargs):
        super(Virtual_Network_LAN_Delete, self).__init__(**kwargs)

        # Request parameters
        self._lan_name = lan_name
        self._lan_owner = lan_owner

    @property
    def lan_name(self):
        return self._lan_name

    @lan_name.setter
    def lan_name(self, value):
        self._lan_name = value

    @property
    def lan_owner(self):
        return self._lan_owner

    @lan_owner.setter
    def lan_owner(self, value):
        self._lan_owner = value

    def pack(self):
        ln_len = len(self._lan_name)
        lo_len = len(self._lan_owner)

        # lan_name_length (int4)
        # lan_name (string,1-8,char36 plus $#@)
        # lan_owner_length (int4)
        # lan_owner (string,1-8,char42)
        #           (string,6,SYSTEM)
        fmt = "!I%dsI%ds" % (ln_len, lo_len)

        buf = struct.pack(fmt,
                          ln_len,
                          bytes(self._lan_name, "UTF-8"),
                          lo_len,
                          bytes(self._lan_owner, "UTF-8"))

        return buf
