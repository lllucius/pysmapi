
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

class Metadata_Space_Query(Smapi_Request_Base):
    def __init__(self,
                 searchkey = b"",
                 **kwargs):
        super(Metadata_Space_Query, self). \
            __init__(b"Metadata_Space_Query", **kwargs)

        # Request parameters
        self._searchkey = searchkey

        # Response values
        self._output_data = []

    @property
    def searchkey(self):
        return self._searchkey

    @searchkey.setter
    def searchkey(self, value):
        self._searchkey = value

    @property
    def output_data(self):
        return self._output_data

    @output_data.setter
    def output_data(self, value):
        self._output_data = value


    def pack(self):
        # searchkey=value (ASCIIZ)
        buf = b"searchkey=%s\x00" % (self._searchkey)

        return super(Metadata_Space_Query, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Metadata_Space_Query, self).unpack(buf, offset)

        buf = buf[offset:]
        offset += len(buf)

        # output_data
        self._output_data = []
        for entry in buf.split(b"\x00"):
            self._output_data.append(entry)

        return offset

