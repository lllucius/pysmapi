
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

class System_Disk_Query(Smapi_Request_Base):
    def __init__(self,
                 dev_num = b"",
                 disk_size = b"",
                 **kwargs):
        super(System_Disk_Query, self). \
            __init__(b"System_Disk_Query", **kwargs)

        # Request parameters
        self._dev_num = dev_num
        self._disk_size = disk_size

        # Response values
        self._disk_info_array = []

    @property
    def dev_num(self):
        return self._dev_num

    @dev_num.setter
    def dev_num(self, value):
        self._dev_num = value

    @property
    def disk_size(self):
        return self._disk_size

    @disk_size.setter
    def disk_size(self, value):
        self._disk_size = value

    @property
    def disk_info_array(self):
        return self._disk_info_array

    @disk_info_array.setter
    def disk_info_array(self, value):
        self._disk_info_array = value

    def pack(self):
        # dev_num=value (string,1-4,char36)
        buf = b"dev_num=%s\x00" % (self._dev_num)

        # disk_size=value (string,0-3,char26)
        if len(self._disk_size) > 0:
            buf += b"disk_size=%s\x00" % (self._disk_size)

        return super(System_Disk_Query, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(System_Disk_Query, self).unpack(buf, offset)

        buf = buf[offset:-1]
        offset -= len(buf)

        # disk_info_array
        for info in buf.split(b"\x00"):
            entry = Obj()
            self._disk_info_array.append(entry)

            info = info.split(b" ")

            # dev_id (string,4,char16)
            entry.dev_id = info[0]

            # dev_type (string,7,char17)
            entry.dev_type = info[1]

            # dev_status (string,1-8,char42)
            entry.dev_status = info[2]

            # dev_volser (string,0-6,char36)
            entry.dev_volser = info[3]

            # disk_size (string,1-8,char10)
            entry.dev_size = info[4] if len(info) == 5 else b""

        return offset

