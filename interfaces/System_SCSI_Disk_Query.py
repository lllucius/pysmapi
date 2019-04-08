
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required scsi_info_array applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

from pysmapi.smapi import Request, Obj

class System_SCSI_Disk_Query(Request):
    def __init__(self,
                 dev_num = "",
                 **kwargs):
        super(System_SCSI_Disk_Query, self).__init__(**kwargs)

        # Request parameters
        self._dev_num = dev_num

        # Response values
        self._scsi_info_array = []
        
    @property
    def dev_num(self):
        return self._dev_num

    @dev_num.setter
    def dev_num(self, value):
        self._dev_num = value

    @property
    def persist(self):
        return self._persist

    @persist.setter
    def persist(self, value):
        self._persist = value

    @property
    def scsi_info_array(self):
        return self._scsi_info_array

    @scsi_info_array.setter
    def scsi_info_array(self, value):
        self._scsi_info_array = value

    def pack(self):
        buf = ""

        # dev_num=value (string,1-4,char36)
        buf += f"dev_num={self._dev_num}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        for info in buf.decode("UTF-8").split("\x00"):
            fields = info.split()

            entry = Obj()
            self._scsi_info_array.append(entry)
        
            entry.dev_id = fields[0]
            entry.dev_type = fields[1]
            entry.dev_attr = fields[2]
            entry.dev_size = fields[3]
            entry.fcp_array = []
            if len(fields) > 4:
                fcp = Obj()
                entry.fcp_array.append(fcp)

                # fcp_dev_id (string,4,char)
                # fcp_dev_wwpn (string,16,char16)
                # fcp_dev_lun (string,16,char16)
                fcp.fcp_dev_id = fields[4][0:4]
                fcp.fcp_dev_wwpn = fields[4][4:4 + 16]
                fcp.fcp_dev_lun = fields[4][4 + 16: 4 + 16 + 16]
