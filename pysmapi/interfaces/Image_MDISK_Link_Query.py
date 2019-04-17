
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

class Image_MDISK_Link_Query(Request):
    def __init__(self,
                 vdev = "",
                 **kwargs):
        super(Image_MDISK_Link_Query, self).__init__(**kwargs)

        # Request parameters
        self._vdev = vdev

        # Response values
        self._link_array = []

    @property
    def vdev(self):
        return self._vdev

    @vdev.setter
    def vdev(self, value):
        self._vdev = value

    @property
    def link_array(self):
        return self._link_array

    @link_array.setter
    def link_array(self, value):
        self._link_array = value

    def pack(self):
        # vdev=value (string,1-4,char36)
        buf = f"vdev={self._vdev}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # link_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # link_array
        for link in b2s(buf[offset:-1]).split("\x00"):
            entry = Obj()
            self._link_array.append(entry)

            # system_name (string,1-8,char42)
            # user (string,1-8,char42)
            # vaddr (string,1-4,char16)
            # access_mode (string,4-5,char26)
            entry.system_name, \
            entry.user, \
            entry.vaddr, \
            entry.access_mode = link.split()

        offset += alen

