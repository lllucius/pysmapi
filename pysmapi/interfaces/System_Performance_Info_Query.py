
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
        self.num_proc = 0
        self.avg_proc = 0
        self.page_rate = 0
        self.total_pages = 0
        self.total_used = 0
        self.monitor_rate = 0
        self.procs = []

    @property
    def monrate(self):
        return self._monrate

    @monrate.setter
    def monrate(self, value):
        self._monrate = value

    @property
    def num_proc(self):
        return self._num_proc

    @num_proc.setter
    def num_proc(self, value):
        self._num_proc = value

    @property
    def avg_proc(self):
        return self._avg_proc

    @avg_proc.setter
    def avg_proc(self, value):
        self._avg_proc = value

    @property
    def page_rate(self):
        return self._page_rate

    @page_rate.setter
    def page_rate(self, value):
        self._page_rate = value

    @property
    def total_pages(self):
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        self._total_pages = value

    @property
    def total_used(self):
        return self._total_used

    @total_used.setter
    def total_used(self, value):
        self._total_used = value

    @property
    def monitor_rate(self):
        return self._monitor_rate

    @monitor_rate.setter
    def monitor_rate(self, value):
        self._monitor_rate = value

    @property
    def procs(self):
        return self._procs

    @procs.setter
    def procs(self, value):
        self._procs = value

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

