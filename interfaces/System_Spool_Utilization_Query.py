
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

class System_Spool_Utilization_Query(Request):
    def __init__(self,
                 **kwargs):
        super(System_Spool_Utilization_Query, self).__init__(**kwargs)

        # Response values
        self._total_spool_pages = 0
        self._total_spool_pages_in_use = 0
        self._total_spool_percent_used = 0
        self._spool_volume_array = []

    @property
    def total_spool_pages(self):
        return self._total_spool_pages

    @total_spool_pages.setter
    def total_spool_pages(self, value):
        self._total_spool_pages = value

    @property
    def total_spool_pages_in_use(self):
        return self._total_spool_pages_in_use

    @total_spool_pages_in_use.setter
    def total_spool_pages_in_use(self, value):
        self._total_spool_pages_in_use = value

    @property
    def total_spool_percent_used(self):
        return self._total_spool_percent_used

    @total_spool_percent_used.setter
    def total_spool_percent_used(self, value):
        self._total_spool_percent_used = value

    @property
    def spool_volume_array(self):
        return self._spool_volume_array

    @spool_volume_array.setter
    def spool_volume_array(self, value):
        self._spool_volume_array = value

    def unpack(self, buf):
        offset = 0

        # spool_information_structure_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4
        
        # spool_information_structure
        sis = buf[offset:offset + alen].decode("UTF-8")
        offset += alen

        # total_spool_pages (string,1-8,char10 plus 'K')
        self._total_spool_pages, _, sis = sis.partition(" ")

        # total_spool_pages_in_use (string,1-8,char10)
        self._total_spool_pages_in_use, _, sis = sis.partition(" ")

        # total_spool_percent_used (string,1-3,char10)
        self._total_spool_percent_used, _, sis = sis.partition(" ")

        self._spool_volume_array = []
        for spool_volume in sis[:-1].split("\x00"):
            entry = Obj()
            self._spool_volume_array.append(entry)

            # volid (string,1-6,char42)
            # rdev (string,1-4,char16)
            # total_pages (string,1-8,char10)
            # pages_in_use (string,1-8,char10)
            # percent_used (string,1-3,char10)
            # dump (string,4-7,char26)
            # drained (string,7-10,char26)
            entry.volid, \
            entry.rdev, \
            entry.total_pages, \
            entry.pages_in_use, \
            entry.percent_used, \
            entry.dump, \
            entry.drained = spool_volume.split(" ")

