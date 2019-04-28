
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

class System_Performance_Info_Query(Request):
    def __init__(self,
                 monrate = "",
                 **kwargs):
        super(System_Performance_Info_Query, self).__init__(**kwargs)

        # Request parameters
        self._monrate = monrate

        # Response values
        self._system_performance_info_data = []

    @property
    def monrate(self):
        return self._monrate

    @monrate.setter
    def monrate(self, value):
        self._monrate = value

    @property
    def system_performance_info_data(self):
        return self._system_performance_info_data

    @system_performance_info_data.setter
    def system_performance_info_data(self, value):
        self._system_performance_info_data = value

    def pack(self):
        buf = ""

        # monrate (string,1-8,char36 plus .)
        if len(self._monrate) > 0:
            buf += f"monrate={self._monrate}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = (len(self._monrate) > 0)
        fields = b2s(buf[:-1]).split("\x00")
        print("fiel", len(fields), offset + 5, fields[5:])
        self.num_proc = int(fields[0])
        self.avg_proc = int(fields[1])
        self.page_rate = int(fields[2])
        self.total_pages = int(fields[3])
        self.total_used = int(fields[4])
        self.monitor_rate = fields[5] if offset else 0
        self.procs = []
        for proc in sorted(fields[5 + offset:]):
            # PROC 0000-033% IFL  VM
            entry = Obj()
            self.procs.append(entry)

            fields = proc.split()
            entry.addr = fields[1][0:4]
            entry.usage = int(fields[1][5:8])
            entry.type = fields[2]
            entry.pe = fields[3]

