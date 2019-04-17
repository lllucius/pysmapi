
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

class Virtual_Network_Vswitch_Query_Byte_Stats(Request):
    def __init__(self,
                 switch_name = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Query_Byte_Stats, self).__init__(**kwargs)

        # Request parameters
        self._switch_name = switch_name

        # Response values
        self._vswitch_array = []

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def vswitch_array(self):
        return self._vswitch_array

    @vswitch_array.setter
    def vswitch_array(self, value):
        self._vswitch_array = value

    def pack(self):
        buf = ""

        # switch_name=value (string,1-8,char42)
        buf += f"switch_name={self._switch_name}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        fields = b2s(buf[offset:-1]).split("\x00")

        count = len(fields)
        i = 1

        self._vswitch_array = []
        while i < count:
            vswitch = Obj()
            self._vswitch_array.append(vswitch)

            vswitch.switch_name, \
            uplink_array_size = fields[i:i + 2]
            i += 2

            vswitch.uplink_array = []
            for j in range(int(uplink_array_size)):
                uplink = Obj()
                vswitch.uplink_array.append(uplink)

                unplink_conn, \
                uplink.uplink_fr_rx, \
                uplink.uplink_fr_rx_dsc, \
                uplink.uplink_fr_rx_err, \
                uplink.uplink_fr_tx, \
                uplink.uplink_fr_tx_dsc, \
                uplink.uplink_fr_tx_dsc_err, \
                uplink.uplink_rx, \
                uplink.uplink_tx = fields[i:i + 9]
                i += 9

            vswitch.bridge_fr_rx, \
            vswitch.bridge_fr_rx_dsc, \
            vswitch.bridge_fr_rx_err, \
            vswitch.bridge_fr_tx, \
            vswitch.bridge_fr_tx_dsc, \
            vswitch.bridge_fr_tx_err, \
            vswitch.bridge_rx, \
            vswitch.bridge_tx, \
            nic_array_size = fields[i:i + 9]
            i += 9

            vswitch.nic_array = []
            for j in range(int(nic_array_size)):
                nic = Obj()
                vswitch.nic_array.append(nic)

                nic.nic_id, \
                nic.nic_fr_rx, \
                nic.nic_fr_rx_dsc, \
                nic.nic_fr_rx_err, \
                nic.nic_fr_tx, \
                nic.nic_fr_tx_dsc, \
                nic.nicr_tx_dsc_err, \
                nic.nic_rx, \
                nic.nic_tx = fields[i:i + 9]
                i += 9

            vlan_array_size = fields[i]
            i += 1

            vswitch.vlan_array = []
            for j in range(int(vlan_array_size)):
                vlan = Obj()
                vswitch.vlan_array.append(vlan)

                vlan.vlan_id, \
                vlan.vlan_rx, \
                vlan.vlan_tx = fields[i:i + 3]
                i += 3

