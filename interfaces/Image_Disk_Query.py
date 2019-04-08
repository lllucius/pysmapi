
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

class Image_Disk_Query(Request):

    # Vdasd access type
    RO = 1
    RW = 2
    vdasd_access_type_names = ["RW"]

    # Vdasd unit
    CYLINDERS = 1
    BLOCKS = 2
    vdasd_unit_names = ["BLOCKS"]

    def __init__(self,
                 vdasd_id = "",
                 **kwargs):
        super(Image_Disk_Query, self).__init__(**kwargs)

        # Request parameters
        self._vdasd_id = vdasd_id

        # Response values
        self._vdasd_array = []

    @property
    def vdasd_id(self):
        return self._vdasd_id

    @vdasd_id.setter
    def vdasd_id(self, value):
        self._vdasd_id = value

    @property
    def vdasd_array(self):
        return self._vdasd_array

    @vdasd_array.setter
    def vdasd_array(self, value):
        self._vdasd_array = value

    def pack(self):
        buf = ""

        # vdasd_id=value (string,1-4,char36)
        buf += "vdasd_id=%s\x00" % (self._vdasd_id)

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # vdasd_array
        buf = buf[offset:]
        alen = len(buf)

        self._vdasd_array = []
        while alen > 0:
            entry = Obj()
            self._vdasd_array.append(entry)

            # vdasd_vdev (string,4,char16)
            # vdasd_rdev (string,4,char16)
            #            (string,4,VDSK)
            # vdasd_access_type (int1)            
            # vdasd_devtype (string,4,char10)
            # vdasd_size (int8)
            # vdasd_unit (int1)
            # vdasd_volid (string,1-6,char37)
            #             (string,6,(TEMP))
            #             (string,6,(VDSK))
            fmt = "!4s4sB4sQB6sB"
            entry.vdasd_vdev, \
            entry.vdasd_rdev, \
            entry.vdasd_access_type, \
            entry.vdasd_devtype, \
            entry.vdasd_size, \
            entry.vdasd_unit, \
            entry.vdasd_volid, \
            asciiz = struct.unpack(fmt, buf[offset:offset + 29])

            offset += 29
            alen -= 29

