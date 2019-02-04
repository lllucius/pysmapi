
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

class System_Page_Utilization_Query(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(System_Page_Utilization_Query, self). \
            __init__(b"System_Page_Utilization_Query", **kwargs)

        # Response values
        self._total_paging_pages = 0
        self._total_paging_pages_in_use = 0
        self._total_paging_percent_used = 0
        self._paging_volume_array = []

    @property
    def total_paging_pages(self):
        return self._total_paging_pages

    @total_paging_pages.setter
    def total_paging_pages(self, value):
        self._total_paging_pages = value

    @property
    def total_paging_pages_in_use(self):
        return self._total_paging_pages_in_use

    @total_paging_pages_in_use.setter
    def total_paging_pages_in_use(self, value):
        self._total_paging_pages_in_use = value

    @property
    def total_paging_percent_used(self):
        return self._total_paging_percent_used

    @total_paging_percent_used.setter
    def total_paging_percent_used(self, value):
        self._total_paging_percent_used = value

    @property
    def paging_volume_array(self):
        return self._paging_volume_array

    @paging_volume_array.setter
    def paging_volume_array(self, value):
        self._paging_volume_array = value

    def unpack(self, buf, offset):
        offset = super(System_Page_Utilization_Query, self).unpack(buf, offset)

        # paging_information_length (int4)
        # paging_information_structure_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4
        
        # paging_information_structure
        sis = buf[offset:offset + alen]
        offset += alen

        # total_paging_pages (string,1-8,char10 plus 'K')
        self._total_paging_pages, _, sis = sis.partition(b" ")

        # total_paging_pages_in_use (string,1-8,char10)
        self._total_paging_pages_in_use, _, sis = sis.partition(b" ")

        # total_paging_percent_used (string,1-3,char10)
        self._total_paging_percent_used, _, sis = sis.partition(b" ")

        for paging_volume in sis[:-1].split(b"\x00"):
            entry = Obj()
            self._paging_volume_array.append(entry)

            paging_volume = paging_volume.split(b" ")

            # volid (string,1-6,char42)
            entry.volid = paging_volume[0]

            # rdev (string,1-4,char16)
            entry.rdev = paging_volume[1] 

            # total_pages (string,1-8,char10)
            entry.total_pages = paging_volume[2]

            # pages_in_use (string,1-8,char10)
            entry.pages_in_use = paging_volume[3]

            # percent_used (string,1-3,char10)
            entry.percent_used = paging_volume[4]

            # drained (string,7-10,char26)
            entry.drained = paging_volume[5]

        return offset

