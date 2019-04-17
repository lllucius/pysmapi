
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

class Image_Definition_Async_Updates(Request):
    def __init__(self,
                 enabled = "",
                 **kwargs):
        super(Image_Definition_Async_Updates, self).__init__(**kwargs)

        # Request parameters
        self._enabled = enabled

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    def pack(self):
        buf = ""

        # enabled=value (string,0-3,char26)
        buf += "enabled=%s\x00" % (self._enabled)

        return s2b(buf)
