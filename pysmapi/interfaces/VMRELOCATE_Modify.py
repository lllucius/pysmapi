
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required max_quiesce applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

from pysmapi.smapi import *

class VMRELOCATE_Modify(Request):
    def __init__(self,
                 max_total = "",
                 max_quiesce = "",
                 **kwargs):
        super(VMRELOCATE_Modify, self).__init__(**kwargs)

        # Request parameters
        self._max_total = max_total
        self._max_quiesce = max_quiesce

        # Response values
        self._VMRELOCATE_error_record = []

    @property
    def max_total(self):
        return self._max_total

    @max_total.setter
    def max_total(self, value):
        self._max_total = value

    @property
    def max_quiesce(self):
        return self._max_quiesce

    @max_quiesce.setter
    def max_quiesce(self, value):
        self._max_quiesce = value

    @property
    def VMRELOCATE_error_record(self):
        return self._VMRELOCATE_error_record

    @VMRELOCATE_error_record.setter
    def VMRELOCATE_error_record(self, value):
        self._VMRELOCATE_error_record = value

    def pack(self):
        buf = ""

        # max_total=value (string,1-8,char42)
        if len(self._max_total) > 0:
            buf += f"max_total={self._max_total}\x00"

        # max_quiesce=value (string,0-6,char42)
        if len(self._max_quiesce) > 0:
            buf += f"max_quiesce={self._max_quiesce}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # VMRELOCATE_error_record (string,1-maxlength,char42 plus blank)
        self._VMRELOCATE_error_record = b2s(buf[offset:-1])
        offset += len(buf)
