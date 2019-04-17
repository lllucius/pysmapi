
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

class Virtual_Network_Adapter_Create(Request):
    # Adapter type
    HIPERSOCKET = 1
    QDIO = 2
    adapter_type_names = {HIPERSOCKET: "HIPERSOCKET", QDIO: "QDIO"}

    def __init__(self,
                 image_device_number = "",
                 adapter_type = 0,
                 network_adapter_devices = 0,
                 channel_path_type_id = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Create, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number
        self._adapter_type = adapter_type
        self._network_adapter_devices = network_adapter_devices
        self._channel_path_type_id = channel_path_type_id

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
    def network_adapter_devices(self):
        return self._network_adapter_devices

    @network_adapter_devices.setter
    def network_adapter_devices(self, value):
        self._network_adapter_devices = value

    @property
    def channel_path_type_id(self):
        return self._channel_path_type_id

    @channel_path_type_id.setter
    def channel_path_type_id(self, value):
        self._channel_path_type_id = value

    def pack(self):
        idn_len = len(self._image_device_number)
        cpti_len = len(self._channel_path_type_id)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)
        # adapter_type (int1)
        # network_adapter_devices (int4; range 3-3072)
        # channel_path_type_id_length (int4)
        # channel_path_type_id (string,0-2,char16)

        fmt = "!I%dsBII%ds" % (idn_len, cpti_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_device_number),
                          self._adapter_type,
                          self._network_adapter_devices,
                          cpti_len,
                          s2b(self._channel_path_type_id))

        return buf
