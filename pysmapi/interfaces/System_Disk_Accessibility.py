
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

class System_Disk_Accessibility(Request):
    def __init__(self,
                 dev_num = "",
                 **kwargs):
        super(System_Disk_Accessibility, self).__init__(**kwargs)

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
        buf = "dev_num=%s\x00" % (self._dev_num)

        return s2b(buf)
