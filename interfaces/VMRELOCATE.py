
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

from pysmapi.smapi import Request, Obj

class VMRELOCATE(Request):
    def __init__(self,
                 destination = "",
                 action = "",
                 force = "",
                 immediate = "",
                 max_total = "",
                 max_quiesce = "",
                 **kwargs):
        super(VMRELOCATE, self).__init__(**kwargs)

        # Request parameters
        self._destination = destination
        self._action = action
        self._force = force
        self._immediate = immediate
        self._max_total = max_total
        self._max_quiesce = max_quiesce

        # Response values
        self._VMRELOCATE_error_record = []

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, value):
        self._force = value

    @property
    def immediate(self):
        return self._immediate

    @immediate.setter
    def immediate(self, value):
        self._immediate = value

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

        # destination=value (string,1-8,char42)
        if len(self._destination) > 0:
            buf += f"destination={self._destination}\x00"

        # action=value (string,0-6,char42)
        if len(self._action) > 0:
            buf += f"action={self._action}\x00"

        # force=value (string,0-27,char42 plus blank)
        if len(self._force) > 0:
            buf += f"force={self._force}\x00"

        # immediate=value (string,0-3,char42)
        if len(self._immediate) > 0:
            buf += f"immediate={self._immediate}\x00"

        # max_total=value (string,0-8,char42)
        if len(self._max_total) > 0:
            buf += f"max_total={self._max_total}\x00"

        # max_quiesce=value (string,0-8,char42)
        if len(self._max_total) > 0:
            buf += f"max_quiesce={self._max_quiesce}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # VMRELOCATE_error_record (string,1-maxlength,char42 plus blank)
        self._VMRELOCATE_error_record = buf[offset:-1].decode("UTF-8")
        offset += len(buf)
