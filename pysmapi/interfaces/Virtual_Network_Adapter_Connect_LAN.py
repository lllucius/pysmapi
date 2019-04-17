
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

class Virtual_Network_Adapter_Connect_LAN(Request):
    def __init__(self,
                 image_device_number = "",
                 lan_name = "",
                 lan_owner = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Connect_LAN, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number
        self._lan_name = lan_name
        self._lan_owner = lan_owner

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def lan_name(self):
        return self._lan_name

    @lan_name.setter
    def lan_name(self, value):
        self._lan_name = value

    @property
    def lan_owner(self):
        return self._lan_owner

    @lan_owner.setter
    def lan_owner(self, value):
        self._lan_owner = value

    def pack(self):
        idn_len = len(self._image_device_number)
        ln_len = len(self._lan_name)
        lo_len = len(self._lan_owner)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)
        # lan_name_length (int4)
        # lan_name (string,1-8,char36 plus $#@)
        # lan_owner_length (int4)
        # lan_owner (string,1-8,char42)

        fmt = "!I%dsI%dsI%ds" % (idn_len, ln_len, lo_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_device_number),
                          ln_len,
                          s2b(self._lan_name),
                          lo_len,
                          s2b(self._lan_owner))

        return buf
