
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required real_device_address applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

from pysmapi.smapi import Request, Obj

class Network_IP_Interface_Query(Request):
    def __init__(self,
                 tcpip_stack = "",
                 interface_all = "",
                 interface_id = "",
                 **kwargs):
        super(Network_IP_Interface_Query, self).__init__(**kwargs)

        # Request parameters
        self._tcpip_stack = tcpip_stack
        self._interface_all = interface_all
        self._interface_id = interface_id

        # Response values
        self._interface_configuration_array = ""

    @property
    def tcpip_stack(self):
        return self._tcpip_stack

    @tcpip_stack.setter
    def tcpip_stack(self, value):
        self._tcpip_stack = value

    @property
    def interface_all(self):
        return self._interface_all

    @interface_all.setter
    def interface_all(self, value):
        self._interface_all = value

    @property
    def interface_id(self):
        return self._interface_id

    @interface_id.setter
    def interface_id(self, value):
        self._interface_id = value

    @property
    def interface_configuration_array(self):
        return self._interface_configuration_array

    @interface_configuration_array.setter
    def interface_configuration_array(self, value):
        self._interface_configuration_array = value

    def pack(self):
        buf = ""

        # tcpip_stack=value (string,1-8,char42)
        if len(self._tcpip_stack) > 0:
            buf += f"tcpip_stack={self._tcpip_stack}\x00"

        # interface_all=value (string,1-8,char42)
        if len(self._interface_all) > 0:
            buf += f"interface_all={self._interface_all}\x00"

        # interface_id=value (string,1-8,char42)
        if len(self._interface_id) > 0:
            buf += f"interface_id={self._interface_id}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # interface_configuration_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        for config in buf[offset:offset + alen].decode("UTF-8").split("\x00"):
            entry = Obj()
            self._interface_configuration_array.append(entry)

            for keyval in config.split():
                key, val = keyval.lower().split("=")
                setattr(entry, key, val)
