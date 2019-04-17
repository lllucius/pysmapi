
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required action applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

from pysmapi.smapi import *

class VMRELOCATE_Status(Request):
    def __init__(self,
                 status_target = "",
                 **kwargs):
        super(VMRELOCATE_Status, self).__init__(**kwargs)

        # Request parameters
        self._status_target = status_target

        # Response values
        self._VMRELOCATE_status_array = []

    @property
    def status_target(self):
        return self._status_target

    @status_target.setter
    def status_target(self, value):
        self._status_target = value

    @property
    def VMRELOCATE_status_array(self):
        return self._VMRELOCATE_status_array

    @VMRELOCATE_status_array.setter
    def VMRELOCATE_status_array(self, value):
        self._VMRELOCATE_status_array = value

    def pack(self):
        buf = ""

        # status_target=value (string,1-8,char42)
        if len(self._status_target) > 0:
            buf += f"status_target={self._status_target}\x00"

        return s2b(buf)

    def unpack(self, buf):
        for status in b2s(buf[:-1]).split("\x00"):
            entry = Obj()
            self._VMRELOCATE_status_array.append(entry)

            fields = status.split()

            # VMRELOCATE_image (string,1-8,char42)
            entry.VMRELOCATE_image = fields[0]

            # VMRELOCATE_source_system (string,1-8,char42)
            entry.VMRELOCATE_source_system = fields[1]

            # VMRELOCATE_destination_system (string,1-8,char42)
            entry.VMRELOCATE_destination_system = fields[2]

            # VMRELOCATE_by (string,1-8,char42
            entry.VMRELOCATE_by = fields[3]

            # VMRELOCATE_elapsed (string,8,char42)
            entry.VMRELOCATE_elapsed = fields[4]

            # VMRELOCATE_status (string,0-15,char26 plus / _)
            entry.VMRELOCATE_status = fields[5]

