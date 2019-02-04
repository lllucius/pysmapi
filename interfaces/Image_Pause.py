
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

class Image_Pause(Smapi_Request_Base):
    def __init__(self,
                 action = b"",
                 **kwargs):
        super(Image_Pause, self). \
            __init__(b"Image_Pause", **kwargs)

        # Request parameters
        self._action = action

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    def pack(self):
        # id=value (string,1-8,char42) (ASCIIZ)
        buf = b"action=%s\x00" % (self._action)

        return super(Image_Pause, self).pack(buf)

