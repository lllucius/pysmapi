
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

class Virtual_Network_Vswitch_Create_Extended(Request):
    def __init__(self,
                 switch_name = "",
                 real_device_address = "",
                 port_name = "",
                 controller_name = "",
                 connection_value = "",
                 queue_memory_limit = "",
                 routing_value = "",
                 transport_type = "",
                 vlan_id = "",
                 port_type = "",
                 persist = "",
                 gvrp_value = "",
                 native_vlanid = "",
                 vswitch_type = "",
                 iptimeout = "",
                 port_selection = "",
                 vswitch_domain = "",
                 vswitch_global = "",
                 group_name = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Create_Extended, self).__init__(**kwargs)

        # Request parameters
        self._switch_name = switch_name
        self._real_device_address = real_device_address
        self._port_name = port_name
        self._controller_name = controller_name
        self._connection_value = connection_value
        self._queue_memory_limit = queue_memory_limit
        self._routing_value = routing_value
        self._transport_type = transport_type
        self._vlan_id = vlan_id
        self._port_type = port_type
        self._persist = persist
        self._gvrp_value = gvrp_value
        self._native_vlanid = native_vlanid
        self._vswitch_type = vswitch_type
        self._iptimeout = iptimeout
        self._port_selection = port_selection
        self._vswitch_domain = vswitch_domain
        self._vswitch_global = vswitch_global
        self._group_name = group_name

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def real_device_address(self):
        return self._real_device_address

    @real_device_address.setter
    def real_device_address(self, value):
        self._real_device_address = value

    @property
    def port_name(self):
        return self._port_name

    @port_name.setter
    def port_name(self, value):
        self._port_name = value

    @property
    def controller_name(self):
        return self._controller_name

    @controller_name.setter
    def controller_name(self, value):
        self._controller_name = value

    @property
    def connection_value(self):
        return self._connection_value

    @connection_value.setter
    def connection_value(self, value):
        self._connection_value = value

    @property
    def queue_memory_limit(self):
        return self._queue_memory_limit

    @queue_memory_limit.setter
    def queue_memory_limit(self, value):
        self._queue_memory_limit = value

    @property
    def routing_value(self):
        return self._routing_value

    @routing_value.setter
    def routing_value(self, value):
        self._routing_value = value

    @property
    def transport_type(self):
        return self._transport_type

    @transport_type.setter
    def transport_type(self, value):
        self._transport_type = value

    @property
    def vlan_id(self):
        return self._vlan_id

    @vlan_id.setter
    def vlan_id(self, value):
        self._vlan_id = value

    @property
    def port_type(self):
        return self._port_type

    @port_type.setter
    def port_type(self, value):
        self._port_type = value

    @property
    def persist(self):
        return self._persist

    @persist.setter
    def persist(self, value):
        self._persist = value

    @property
    def gvrp_value(self):
        return self._gvrp_value

    @gvrp_value.setter
    def gvrp_value(self, value):
        self._gvrp_value = value

    @property
    def native_vlanid(self):
        return self._native_vlanid

    @native_vlanid.setter
    def native_vlanid(self, value):
        self._native_vlanid = value

    @property
    def vswitch_type(self):
        return self._vswitch_type

    @vswitch_type.setter
    def vswitch_type(self, value):
        self._vswitch_type = value

    @property
    def iptimeout(self):
        return self._iptimeout

    @iptimeout.setter
    def iptimeout(self, value):
        self._iptimeout = value

    @property
    def port_selection(self):
        return self._port_selection

    @port_selection.setter
    def port_selection(self, value):
        self._port_selection = value

    @property
    def vswitch_domain(self):
        return self._vswitch_domain

    @vswitch_domain.setter
    def vswitch_domain(self, value):
        self._vswitch_domain = value

    @property
    def vswitch_global(self):
        return self._vswitch_global

    @vswitch_global.setter
    def vswitch_global(self, value):
        self._vswitch_global = value

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    def pack(self):
        buf = ""

        # switch_name=value (string,1-8,char42)
        buf += f"switch_name={self._switch_name}\x00"

        # real_device_address=value (string,0-6,char42)
        if len(self._real_device_address) > 0:
            buf += f"real_device_address={self._real_device_address}\x00"

        # port_name=value (string,0-27,char42 plus blank)
        if len(self._port_name) > 0:
            buf += f"port_name={self._port_name}\x00"

        # controller_name=value (string,0-8,char42)
        #                       (string,1,*)
        if len(self._controller_name) > 0:
            buf += f"controller_name={self._controller_name}\x00"

        # connection_value=value (string,0-10,char42)
        if len(self._connection_value) > 0:
            buf += f"connection_value={self._connection_value}\x00"

        # queue_memory_limit=value (string,0-1,char16; range 1-8)
        if len(self._queue_memory_limit) > 0:
            buf += f"queue_memory_limit={self._queue_memory_limit}\x00"

        # routing_value=value (string,0-9,char42)
        if len(self._routing_value) > 0:
            buf += f"routing_value={self._routing_value}\x00"

        # transport_type=value (string,0-8,char42)
        if len(self._transport_type) > 0:
            buf += f"transport_type={self._transport_type}\x00"

        # vlan_id=value (string,0-8,char42)
        if len(self._vlan_id) > 0:
            buf += f"vlan_id={self._vlan_id}\x00"

        # port_type=value (string,0-6,char42)
        if len(self._port_type) > 0:
            buf += f"port_type={self._port_type}\x00"

        # persist=value (string,0-3,char42)
        if len(self._persist) > 0:
            buf += f"persist={self._persist}\x00"

        # gvrp_value=value (string,0-6,char42)
        if len(self._gvrp_value) > 0:
            buf += f"gvrp_value={self._gvrp_value}\x00"

        # native_vlanid=value (string,0-4,char42)
        if len(self._native_vlanid) > 0:
            buf += f"native_vlanid={self._native_vlanid}\x00"

        # vswitch_type=value (string,0-4,char42)
        if len(self._vswitch_type) > 0:
            buf += f"vswitch_type={self._vswitch_type}\x00"

        # iptimeout=value (string,0-3,char10)
        if len(self._iptimeout) > 0:
            buf += f"iptimeout={self._iptimeout}\x00"

        # port_selection=value (string,0-9,char26)
        if len(self._port_selection) > 0:
            buf += f"port_selection={self._port_selection}\x00"

        # group_name=value (string,1-8,char36 plus @#$_)
        if len(self._group_name) > 0:
            buf += f"group_name={self._group_name}\x00"

        # vswitch_domain=value (string,0-1,char26; range A-H)
        if len(self._vswitch_domain) > 0:
            buf += f"vswitch_domain={self._vswitch_domain}\x00"

        # vswitch_global=value (string,3-6,char26)
        if len(self._vswitch_global) > 0:
            buf += f"vswitch_global={self._vswitch_global}\x00"

        return s2b(buf)

