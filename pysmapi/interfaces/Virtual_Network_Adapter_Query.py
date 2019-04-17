
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

class Virtual_Network_Adapter_Query(Request):
    # Adapter type
    HIPERSOCKETS = 1
    QDIO = 2
    adapter_type_names = {HIPERSOCKETS: "HIPERSOCKET", QDIO: "QDIO"}

    # Adapter status
    NOTCOUPLED = 0
    NOTACTIVE = 1
    ACTIVE = 2
    adapter_status_names = {NOTCOUPLED: "NOT COUPLED", NOTACTIVE: "NOT ACTIVE", ACTIVE: "ACTIVE"}

    def __init__(self,
                 image_device_number = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Query, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number

        # Response values
        self._adapter_array = []

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def adapter_array(self):
        return self._adapter_array

    @adapter_array.setter
    def adapter_array(self, value):
        self._adapter_array = value

    def pack(self):
        idn_len = len(self._image_device_number)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)

        fmt = "!I%ds" % (idn_len)

        buf = struct.pack(fmt,
                          idn_len,
                          s2b(self._image_device_number))

        return buf

    def unpack(self, buf):
        offset = 0

        # adapter_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._adapter_array = []
        while alen > 0:
            entry = Obj()
            self._adapter_array.append(entry)

            # adapter_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # image_device_number_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # image_device_number (string,1-8,char36 plus $#@)
            entry.image_device_number = b2s(buf[offset:offset + nlen])
            offset += nlen

            # adapter_type=(int1)
            # network_adapter_devices (int4)
            # adapter_status (int1)
            entry.adapter_type, \
            entry.network_adapter_devices, \
            entry.adapter_status = struct.unpack("!BIB", buf[offset:offset + 6])
            offset += 6

            # lan_owner_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # lan_owner (string,1-8,char36 plus $#@)
            entry.lan_owner = b2s(buf[offset:offset + nlen])
            offset += nlen

            # lan_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # lan_name (string,1-8,char36 plus $#@)
            entry.lan_name = b2s(buf[offset:offset + nlen])
            offset += nlen


