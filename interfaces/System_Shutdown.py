
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

from base import Smapi_Request_Base, Obj

class System_Shutdown(Smapi_Request_Base):
    def __init__(self,
                 within = b"",
                 by = b"",
                 immediate = b"",
                 reipl = b"",
                 cancel = b"",
                 **kwargs):
        super(System_Shutdown, self). \
            __init__(b"System_Shutdown", **kwargs)

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
        parms = []

        # Within=value (string,0-5,char10)
        if len(self._within) > 0:
            parms.append("within=%s" % (self._within))

        # By=value (string,0-8,char10 plus :)
        if len(self._by) > 0:
            parms.append("by=%s" % (self._by))

        # Immediate=value (string,0-11,char36)
        if len(self._immediate) > 0:
            parms.append("immediate=%s" % (self._immediate))

        # Reipl=value (string,0-7,char26)
        if len(self._reipl) > 0:
            parms.append("reipl=%s" % (self._reipl))

        # Cancel=value (string,0-8,char26)
        if len(self._cancel) > 0:
            parms.append("cancel=%s" % (self._cancel))

        buf = (" ".join(parms)) + "\x00"

        return super(System_Shutdown, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(System_Shutdown, self).unpack(buf, offset)

        # error_data_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # error_data (string) (ASCIIZ)
        self._error_data = buf[offset:offset + alen - 1]
        offset += alen

        return offset

