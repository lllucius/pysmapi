
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

from pysmapi.smapi import *

class Network_IP_Interface_Modify(Request):
    def __init__(self,
                 tcpip_stack = "",
                 interface_id = "",
                 permanent = "",
                 delete_ip = "",
                 add_ip = "",
                 change_mask = "",
                 change_mtu = "",
                 change_p2p = "",
                 **kwargs):
        super(Network_IP_Interface_Modify, self).__init__(**kwargs)

        # Request parameters
        self._tcpip_stack = tcpip_stack
        self._interface_id = interface_id
        self._permanent = permanent
        self._delete_ip = delete_ip
        self._add_ip = add_ip
        self._change_mask = change_mask
        self._change_mtu = change_mtu
        self._change_p2p = change_p2p

        # Response values
        self._error_data = ""

    @property
    def tcpip_stack(self):
        return self._tcpip_stack

    @tcpip_stack.setter
    def tcpip_stack(self, value):
        self._tcpip_stack = value

    @property
    def interface_id(self):
        return self._interface_id

    @interface_id.setter
    def interface_id(self, value):
        self._interface_id = value

    @property
    def permanent(self):
        return self._permanent

    @permanent.setter
    def permanent(self, value):
        self._permanent = value

    @property
    def delete_ip(self):
        return self._delete_ip

    @delete_ip.setter
    def delete_ip(self, value):
        self._delete_ip = value

    @property
    def add_ip(self):
        return self._add_ip

    @add_ip.setter
    def add_ip(self, value):
        self._add_ip = value

    @property
    def change_mask(self):
        return self._change_mask

    @change_mask.setter
    def change_mask(self, value):
        self._change_mask = value

    @property
    def change_mtu(self):
        return self._change_mtu

    @change_mtu.setter
    def change_mtu(self, value):
        self._change_mtu = value

    @property
    def change_p2p(self):
        return self._change_p2p

    @change_p2p.setter
    def change_p2p(self, value):
        self._change_p2p = value

    @property
    def error_data(self):
        return self._error_data

    @error_data.setter
    def error_data(self, value):
        self._error_data = value

    def pack(self):
        buf = ""

        # tcpip_stack=value (string,1-8,char42)
        if len(self._tcpip_stack) > 0:
            buf += f"tcpip_stack={self._tcpip_stack}\x00"

        # interface_id=value (string,1-16,charNB)
        if len(self._interface_id) > 0:
            buf += f"interface_id={self._interface_id}\x00"

        # permanent=value (string,0-3,char26)
        if len(self._permanent) > 0:
            buf += f"permanent={self._permanent}\x00"

        # delete_ip=value (string,3-43,char16 plus ':', '.' and '/')
        if len(self._delete_ip) > 0:
            buf += f"delete_ip={self._delete_ip}\x00"

        # add_ip=value (string,3-43,char16 plus ':', '.' and '/')
        if len(self._add_ip) > 0:
            buf += f"add_ip={self._add_ip}\x00"

        # change_mask=value (string,7-15,charNB)
        if len(self._change_mask) > 0:
            buf += f"change_mask={self._change_mask}\x00"

        # change_mtu=value (string,1-5,char10)
        if len(self._change_mtu) > 0:
            buf += f"change_mtu={self._change_mtu}\x00"

        # change_p2p=value (string,7-15,charNB)
        if len(self._change_p2p) > 0:
            buf += f"change_p2p={self._change_p2p}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # error_data_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # error_data (string) (ASCIIZ)
        self._error_data = b2s(buf[offset:offset + alen])


