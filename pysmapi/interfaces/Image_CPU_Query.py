
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

class Image_CPU_Query(Request):
    # CPU base
    BASE = 1
    NOT_BASE = 2
    cpu_base_names = {BASE: "BASE", NOT_BASE: "NOT BASE"}

    # CPU status
    STOPPED = 1
    CHECK_STOPPED = 2
    SOFT_STOPPED_OR_ACTIVE = 3
    cpu_status_names = {STOPPED: "STOPPED", CHECK_STOPPED: "CHECK_STOPPED", SOFT_STOPPED_OR_ACTIVE: "SOFT-STOPPED OR ACTIVE"}

    # CPU type
    CP = 1
    IFL = 2
    ZAAP = 3
    ZIIP = 4
    cpu_type_names = {CP: "CP", IFL: "IFL", ZAAP: "ZAAP", ZIIP: "ZIIP"}

    def __init__(self,
                 **kwargs):
        super(Image_CPU_Query, self).__init__(**kwargs)

        # Response values
        self._number_cpus = 0
        self._cpu_info_array = []

    @property
    def number_cpus(self):
        return self._number_cpus

    @number_cpus.setter
    def number_cpus(self, value):
        self._number_cpus = value

    @property
    def cpu_info_array(self):
        return self._cpu_info_array

    @cpu_info_array.setter
    def cpu_info_array(self, value):
        self._cpu_info_array = value

    def unpack(self, buf):
        offset = 0

        # number_CPUs (int4)
        # CPU_info_array_length (int4)
        self._number_cpus, \
        alen = struct.unpack("!II", buf[offset:offset + 8])
        offset += 8

        self._cpu_info_array = []
        while alen > 0:
            entry = Obj()
            self._cpu_info_array.append(entry)

            # CPU_info_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # CPU_number (int4)
            # CPU_id_length (int4)
            entry.cpu_number, \
            nlen = struct.unpack("!II", buf[offset:offset + 8])
            offset += 8

            # CPU_id (string,1-16,char16)
            entry.cpu_id = b2s(buf[offset:offset + nlen])
            offset += nlen

            # CPU_base (int1)
            entry.cpu_base = buf[offset]
            offset += 1

            # CPU_status (int1)
            entry.cpu_status = buf[offset]
            offset += 1

            # CPU_type (int1)
            entry.cpu_type = buf[offset]
            offset += 1

