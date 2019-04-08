
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

class System_Shutdown(Request):
    def __init__(self,
                 within = "",
                 by = "",
                 immediate = "",
                 reipl = "",
                 cancel = "",
                 **kwargs):
        super(System_Shutdown, self).__init__(**kwargs)

        # Request parameters
        self._within = within
        self._by = by
        self._immediate = immediate
        self._reipl = reipl
        self._cancel = cancel

        # Response values
        self._error_data = []

    @property
    def within(self):
        return self._within

    @within.setter
    def within(self, value):
        self._within = value

    @property
    def by(self):
        return self._by

    @by.setter
    def by(self, value):
        self._by = value

    @property
    def immediate(self):
        return self._immediate

    @immediate.setter
    def immediate(self, value):
        self._immediate = value

    @property
    def reipl(self):
        return self._reipl

    @reipl.setter
    def reipl(self, value):
        self._reipl = value

    @property
    def cancel(self):
        return self._cancel

    @cancel.setter
    def cancel(self, value):
        self._cancel = value

    @property
    def error_data(self):
        return self._error_data

    @error_data.setter
    def error_data(self, value):
        self._error_data = value

    def pack(self):
        buf = []

        # Within=value (string,0-5,char10)
        if len(self._within) > 0:
            buf += f"within={self._within}\x00"

        # By=value (string,0-8,char10 plus :)
        if len(self._by) > 0:
            buf += f"by={self._by}\x00"

        # Immediate=value (string,0-11,char36)
        if len(self._immediate) > 0:
            buf += f"immediate={self._immediate}\x00"

        # Reipl=value (string,0-7,char26)
        if len(self._reipl) > 0:
            buf += f"reipl={self._reipl}\x00"

        # Cancel=value (string,0-8,char26)
        if len(self._cancel) > 0:
            buf += f"cancel={self._cancel}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # error_data_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # error_data (string) (ASCIIZ)
        self._error_data = buf[offset:offset + alen - 1].decode("UTF-8")
        offset += alen

