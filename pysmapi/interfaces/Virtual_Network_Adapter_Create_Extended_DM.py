
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

class Virtual_Network_Adapter_Create_Extended_DM(Request):
    def __init__(self,
                 image_device_number = "",
                 adapter_type = "",
                 devices = "",
                 channel_path_id = "",
                 mac_id = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Create_Extended_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number
        self._adapter_type = adapter_type
        self._devices = devices
        self._channel_path_id = channel_path_id
        self._mac_id = mac_id

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def adapter_type(self):
        return self._adapter_type

    @adapter_type.setter
    def adapter_type(self, value):
        self._adapter_type = value

    @property
    def devices(self):
        return self._devices

    @devices.setter
    def devices(self, value):
        self._devices = value

    @property
    def channel_path_id(self):
        return self._channel_path_id

    @channel_path_id.setter
    def channel_path_id(self, value):
        self._channel_path_id = value

    @property
    def mac_id(self):
        return self._mac_id

    @mac_id.setter
    def mac_id(self, value):
        self._mac_id = value

    def pack(self):
        buf = ""

        # image_device_number (string,1-8,char42)
        if len(self._image_device_number) > 0:
            buf += f"image_device_number={self._image_device_number}\x00"

        # adapter_type (string,1-8,char42)
        if len(self._adapter_type) > 0:
            buf += f"adapter_type={self._adapter_type}\x00"

        # devices (string,1-8,char42)
        if len(self._devices) > 0:
            buf += f"devices={self._devices}\x00"

        # channel_path_id (string,1-8,char42)
        if len(self._channel_path_id) > 0:
            buf += f"channel_path_id={self._channel_path_id}\x00"

        # mac_id (string,1-8,char42)
        if len(self._mac_id) > 0:
            buf += f"mac_id={self._mac_id}\x00"

        # adapter_create_names_length (int4)
        return struct.pack("!I", len(buf)) + s2b(buf)

