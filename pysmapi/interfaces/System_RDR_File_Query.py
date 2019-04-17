
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

class System_RDR_File_Query(Request):
    def __init__(self,
                 **kwargs):
        super(System_RDR_File_Query, self).__init__(**kwargs)

        # Response values
        self._reader_file_info = []

    @property
    def reader_file_info(self):
        return self._reader_file_info

    @reader_file_info.setter
    def reader_file_info(self, value):
        self._reader_file_info = value

    def unpack(self, buf):
        self._reader_file_info = []

        # rdr_file_info (string, 1-80, char44)
        for rdr in b2s(buf[:-1]).split("\x00"):
            entry = Obj()
            self._reader_file_info.append(entry)

            # ORIGINID FILE CLASS RECORDS CPY HOLD DATE TIME NAME TYPE DIST
            entry.originid = rdr[0:8].rstrip()
            entry.file = rdr[9:13].rstrip()
            entry.cls = rdr[14].rstrip()
            entry.records = rdr[20:28].rstrip()
            entry.cpy = rdr[29:32].rstrip()
            entry.hold = rdr[33:37].rstrip()
            entry.date = rdr[38:43].rstrip()
            entry.time = rdr[44:52].rstrip()
            entry.name = rdr[53:62].rstrip()
            entry.type = rdr[63:71].rstrip()
            entry.dist = rdr[72:80].rstrip()

