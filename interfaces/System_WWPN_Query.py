
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

class System_WWPN_Query(Request):

    # dev status
    ACTIVE = 1
    FREE = 2
    OFFLINE = 3
    dev_status_names = ["OFFLINE"]

    def __init__(self,
                 owner = "",
                 **kwargs):
        super(System_WWPN_Query, self).__init__(**kwargs)

        # Request parameters
        self._owner = owner

        # Response values
        self._wwpn_array = []

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    @property
    def wwpn_array(self):
        return self._wwpn_array

    @wwpn_array.setter
    def wwpn_array(self, value):
        self._wwpn_array = value

    def pack(self):
        # owner=value (string,0-3,char26) (ASCIIZ)
        buf = "owner=%s\x00" % (self._owner)

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        # wwpn_array
        self._wwpn_array = []
        for wwpn in buf[:-1].decode("UTF-8").split("\x00"):
            entry = Obj()
            self._wwpn_array.append(entry)

            wwpn = wwpn.split(" ")

            # fcp_dev_id (string,4,char16)
            entry.fcp_dev_id = wwpn[0]

            # npiv_wwpn (string,4-16,char16)
            entry.npiv_wwpn = wwpn[1]

            # chpid (string,2,char16)
            entry.chpid = wwpn[2]

            # perm_wwpn (string,16,char16)
            entry.perm_wwpn = wwpn[3]

            # dev_status (string,1,char10)
            entry.dev_status = wwpn[4]

            # owner (string,1-8,char42)
            entry.owner = wwpn[5]

