
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

class Virtual_Network_Adapter_Connect_Vswitch_Extended(Request):
    def __init__(self,
                 image_device_number = "",
                 switch_name = "",
                 port_selection = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Connect_Vswitch_Extended, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number
        self._switch_name = switch_name
        self._port_selection = port_selection

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def port_selection(self):
        return self._port_selection

    @port_selection.setter
    def port_selection(self, value):
        self._port_selection = value


    def pack(self):
        buf = ""

        # image_device_number=value (string,1-8,char36 plus @#$_)
        if len(self._image_device_number) > 0:
            buf += f"image_device_number={self._image_device_number}\x00"

        # switch_name=value (string,1-8,char36 plus @#$_)
        if len(self._switch_name) > 0:
            buf += f"switch_name={self._switch_name}\x00"

        # port_selection=value (string,1-8,char36 plus @#$_)
        if len(self._port_selection) > 0:
            buf += f"port_selection={self._port_selection}\x00"

        return s2b(buf)
