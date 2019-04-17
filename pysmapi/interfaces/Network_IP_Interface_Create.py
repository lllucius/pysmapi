
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

class Network_IP_Interface_Create(Request):
    def __init__(self,
                 tcpip_stack = "",
                 interface_id = "",
                 permanent = "",
                 primary_ipv4 = "",
                 primary_ipv6 = "",
                 interface = "",
                 cpu = "",
                 transport_type = "",
                 mtu = "",
                 noforward = "",
                 pathmtu = "",
                 p2p = "",
                 port_name = "",
                 port_number = "",
                 vlan = "",
                 **kwargs):
        super(Network_IP_Interface_Create, self).__init__(**kwargs)

        # Request parameters
        self._tcpip_stack = tcpip_stack
        self._interface_id = interface_id
        self._permanent = permanent
        self._primary_ipv4 = primary_ipv4
        self._primary_ipv6 = primary_ipv6
        self._interface = interface
        self._cpu = cpu
        self._transport_type = transport_type
        self._mtu = mtu
        self._noforward = noforward
        self._pathmtu = pathmtu
        self._p2p = p2p
        self._port_name = port_name
        self._port_number = port_number
        self._vlan = vlan

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
    def primary_ipv4(self):
        return self._primary_ipv4

    @primary_ipv4.setter
    def primary_ipv4(self, value):
        self._primary_ipv4 = value

    @property
    def primary_ipv6(self):
        return self._primary_ipv6

    @primary_ipv6.setter
    def primary_ipv6(self, value):
        self._primary_ipv6 = value

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, value):
        self._interface = value

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, value):
        self._cpu = value

    @property
    def transport_type(self):
        return self._transport_type

    @transport_type.setter
    def transport_type(self, value):
        self._transport_type = value

    @property
    def mtu(self):
        return self._mtu

    @mtu.setter
    def mtu(self, value):
        self._mtu = value

    @property
    def noforward(self):
        return self._noforward

    @noforward.setter
    def noforward(self, value):
        self._noforward = value

    @property
    def pathmtu(self):
        return self._pathmtu

    @pathmtu.setter
    def pathmtu(self, value):
        self._pathmtu = value

    @property
    def p2p(self):
        return self._p2p

    @p2p.setter
    def p2p(self, value):
        self._p2p = value

    @property
    def port_name(self):
        return self._port_name

    @port_name.setter
    def port_name(self, value):
        self._port_name = value

    @property
    def port_number(self):
        return self._port_number

    @port_number.setter
    def port_number(self, value):
        self._port_number = value

    @property
    def vlan(self):
        return self._vlan

    @vlan.setter
    def vlan(self, value):
        self._vlan = value

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

        # primary_ipv4=value (string,7-18,char10 plus '.' and '/')
        if len(self._primary_ipv4) > 0:
            buf += f"primary_ipv4={self._primary_ipv4}\x00"

        # primary_ipv6=value (string,3-43,char16 plus ':' and '/')
        if len(self._primary_ipv6) > 0:
            buf += f"primary_ipv6={self._primary_ipv6}\x00"

        # interface=value (string,4-37,char)
        if len(self._interface) > 0:
            buf += f"interface={self._interface}\x00"

        # cpu=value (string,0-1,char10)
        if len(self._cpu) > 0:
            buf += f"cpu={self._cpu}\x00"

        # transport_type=value (string,2-8,char26)
        if len(self._transport_type) > 0:
            buf += f"transport_type={self._transport_type}\x00"

        # mtu=value (string,0-5,char10)
        if len(self._mtu) > 0:
            buf += f"mtu={self._mtu}\x00"

        # noforward=value (string,0-3,char26)
        if len(self._noforward) > 0:
            buf += f"noforward={self._noforward}\x00"

        # pathmtu=value (string,0-3,char26)
        if len(self._pathmtu) > 0:
            buf += f"pathmtu={self._pathmtu}\x00"

        # p2p=value (string,7-15,char10 plus '.')
        if len(self._p2p) > 0:
            buf += f"p2p={self._p2p}\x00"

        # port_name=value (string,1-8,charNB)
        if len(self._port_name) > 0:
            buf += f"port_name={self._port_name}\x00"

        # port_number=value (string,1-2,char10)
        if len(self._port_number) > 0:
            buf += f"port_number={self._port_number}\x00"

        # vlan=value (string,1-9,char10 plus blank)
        if len(self._vlan) > 0:
            buf += f"vlan={self._vlan}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # error_data_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # error_data (string) (ASCIIZ)
        self._error_data = b2s(buf[offset:offset + alen])

