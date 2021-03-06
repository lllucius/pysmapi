
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

class System_FCP_Free_Query(Request):

    # dev status
    ACTIVE = 1
    FREE = 2
    OFFLINE = 3
    dev_status_names = {ACTIVE: "ACTIVE", FREE: "FREE", OFFLINE: "OFFLINE"}

    def __init__(self,
                 fcp_dev = "",
                 **kwargs):
        super(System_FCP_Free_Query, self).__init__(**kwargs)

        # Request parameters
        self._fcp_dev = fcp_dev

        # Response values
        self._fcp_array = []

    @property
    def fcp_dev(self):
        return self._fcp_dev

    @fcp_dev.setter
    def fcp_dev(self, value):
        self._fcp_dev = value

    @property
    def fcp_array(self):
        return self._fcp_array

    @fcp_array.setter
    def fcp_array(self, value):
        self._fcp_array = value

    def pack(self):
        # fcp_dev=value (string,1-4,char16) (ASCIIZ)
        buf = "fcp_dev=%s\x00" % (self._fcp_dev)

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # fcp_array
        buf = buf[offset:]
        offset += len(buf)

        self._fcp_array = []
        for fcp in b2s(buf[:-1]).split("\x00"):
            entry = Obj()
            self._fcp_array.append(entry)

            fcp = fcp.split(";")

            # fcp_dev (string,4,char16)
            entry.fcp_Dev = fcp[0]

            # wwpn (string,16,char16)
            entry.wwpn = fcp[1]

            # lun (string,16,char16)
            entry.lun = fcp[2]

            # uuid (string,32-64,char16)
            entry.uuid = fcp[3]

            # vendor (string,1-8,char42)
            entry.vendor = fcp[4]

            # prod (string,1-4,char10)
            entry.prod = fcp[5]

            # model (string,1-4,char10)
            entry.model = fcp[6]

            # serial (string,1-8,char10)
            entry.serial = fcp[7]

            # code (string,1-4,char10)
            entry.code = fcp[8]

            # blk_size (string,1-10,char10)
            entry.blk_size = fcp[9]

            # diskblks (string,1-10,char10)
            entry.diskblks = fcp[10]

            # lun_size (string,1-20,char10)
            entry.lun_size = fcp[11]

