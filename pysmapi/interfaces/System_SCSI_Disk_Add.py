
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required dev_path_array applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

from pysmapi.smapi import *

class System_SCSI_Disk_Add(Request):
    def __init__(self,
                 dev_num = "",
                 dev_path_array = "",
                 option = "",
                 persist = "",
                 **kwargs):
        super(System_SCSI_Disk_Add, self).__init__(**kwargs)

        # Request parameters
        self._dev_num = dev_num
        self._dev_path_array = dev_path_array
        self._option = option
        self._persist = persist

    @property
    def dev_num(self):
        return self._dev_num

    @dev_num.setter
    def dev_num(self, value):
        self._dev_num = value

    @property
    def dev_path_array(self):
        return self._dev_path_array

    @dev_path_array.setter
    def dev_path_array(self, value):
        self._dev_path_array = value

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, value):
        self._option = value

    @property
    def persist(self):
        return self._persist

    @persist.setter
    def persist(self, value):
        self._persist = value

    def pack(self):
        buf = ""

        # dev_num=value (string,1-4,char16)
        buf += f"dev_num={self._dev_num}\x00"

        # dev_path_array=fcp_dev_num (string,1-4,char16) <blank>
        #                fcp_dev_num (string,1-4,char16) <blank>
        #                fcp_lun (string,1-16,char16) <semicolon>
        #                ...
        buf += f"dev_path_array={self._dev_path_array}\x00"

        # option=value (string,0-1,char10)
        if len(self._option) > 0:
            buf += f"option={self._option}\x00"

        # persist=value (string,0-3,char42)
        if len(self._persist) > 0:
            buf += f"persist={self._persist}\x00"

        return s2b(buf)

