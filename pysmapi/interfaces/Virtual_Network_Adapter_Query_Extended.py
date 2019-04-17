
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

class Virtual_Network_Adapter_Query_Extended(Request):
    def __init__(self,
                 image_device_number = "",
                 **kwargs):
        super(Virtual_Network_Adapter_Query_Extended, self).__init__(**kwargs)

        # Request parameters
        self._image_device_number = image_device_number

        # Response values
        self._virtual_network_adapter_data = []

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def virtual_network_adapter_data(self):
        return self._virtual_network_adapter_data

    @virtual_network_adapter_data.setter
    def virtual_network_adapter_data(self, value):
        self._virtual_network_adapter_data = value

    def pack(self):
        buf = ""

        # image_device_number (string,0-4,char16)
        if len(self._image_device_number) > 0:
            buf += f"image_device_number={self._image_device_number}\x00"

        # virtual_network_adapter_query_names_length (int4)
        return struct.pack("!I", len(buf)) + s2b(buf)

    def unpack(self, buf):
        offset = 0

        # virtual_network_adapter_data_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._virtual_network_adapter_data = []

        entry = None
        data = b2s(buf[offset:offset + alen - 1]).split("\x00")
        for rec in data:
            kv = rec.split("=")

            if kv[0] == "adapter_address":
                adapter = Obj()
                self._virtual_network_adapter_data.append(adapter)

                adapter.adapter_address = \
                adapter.adapter_status = \
                adapter.adapter_type = \
                adapter.device_options = \
                adapter.extended_port_status = \
                adapter.lan_name = \
                adapter.lan_owner = \
                adapter.network_device_count = \
                adapter.port_type = \
                adapter.router_status = None

                adapter.mac_addresses = []

                entry = adapter
            elif kv[0] == "mac_address":
                mac = Obj()
                adapter.mac_addresses.append(mac)

                mac.mac_address = \
                mac.mac_address_type =\
                mac.mac_ip_address = \
                mac.mac_ip_version = \
                mac.mac_status = None

                entry = mac
            elif kv[0] in ["adapter_count", "mac_count"]:
                continue
            elif kv[0] in "mac_info_end":
                entry = adapter
                continue
            elif kv[0] == "adapter_info_end":
                entry = None
                continue
            elif len(kv) == 1:
                continue

            setattr(entry, kv[0], kv[1])

