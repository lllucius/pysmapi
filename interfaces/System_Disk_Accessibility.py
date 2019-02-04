
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

class System_Disk_Accessibility(Smapi_Request_Base):
    def __init__(self,
                 dev_num = b"",
                 **kwargs):
        super(System_Disk_Accessibility, self). \
            __init__(b"System_Disk_Accessibility", **kwargs)

        # Request parameters
        self._dev_num = dev_num

    @property
    def dev_num(self):
        return self._dev_num

    @dev_num.setter
    def dev_num(self, value):
        self._dev_num = value

    def pack(self):
        # dev_num=value (string,1-4,char36)
        buf = b"dev_num=%s\x00" % (self._dev_num)

        return super(System_Disk_Accessibility, self).pack(buf)

