
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

class System_RDR_File_Manage(Request):
    def __init__(self,
                 spoolids = "",
                 action = "",
                 **kwargs):
        super(System_RDR_File_Manage, self).__init__(**kwargs)

        # Request parameters
        self._spoolids = spoolids
        self._action = action

    @property
    def spoolids(self):
        return self._spoolids

    @spoolids.setter
    def spoolids(self, value):
        self._spoolids = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    def pack(self):
        buf = ""

        # spoolids=value (string,1-4,char10)
        #                (string,3,char26) ALL
        buf += "spoolids=%s\x00" % (self._spoolids)

        # action=value (string,5,char26) PURGE
        #              (string,5,char26) ORDER
        #              (string,8,char26) TRANSFER
        buf += "action=%s\x00" % (self._action)

        return bytes(buf, "UTF-8")
