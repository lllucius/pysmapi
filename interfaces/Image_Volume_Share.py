
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

class Image_Volume_Share(Request):
    def __init__(self,
                 img_vol_addr = "",
                 share_enable = "",
                 **kwargs):
        super(Image_Volume_Share, self).__init__(**kwargs)

        # Request parameters
        self._img_vol_addr = img_vol_addr
        self._share_enable = share_enable

    @property
    def img_vol_addr(self):
        return self._img_vol_addr

    @img_vol_addr.setter
    def img_vol_addr(self, value):
        self._img_vol_addr = value

    @property
    def share_enable(self):
        return self._share_enable

    @share_enable.setter
    def share_enable(self, value):
        self._share_enable = value

    def pack(self):
        # img_vol_addr=value (string,1-4,char36)
        buf = "img_vol_addr=%s\x00" % (self._img_vol_addr)
        
        # share_enable=value (string,0-3,char26)
        if len(self._share_enable) > 0:
            buf += "share_enable=\x00" % (self._share_enable)

        return bytes(buf, "UTF-8")
