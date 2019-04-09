
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

class Virtual_Network_VLAN_Query_Stats(Request):
    def __init__(self,
                 userid = "",
                 vlan_id = "",
                 device = "",
                 fmt_version = "",
                 **kwargs):
        super(Virtual_Network_VLAN_Query_Stats, self).__init__(**kwargs)

        # Request parameters
        self._userid = userid
        self._vlan_id = vlan_id
        self._device = device
        self._fmt_version = fmt_version

        # Response values
        self._port_nic_array = []

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, value):
        self._userid = value

    @property
    def vlan_id(self):
        return self._vlan_id

    @vlan_id.setter
    def vlan_id(self, value):
        self._vlan_id = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def fmt_version(self):
        return self._fmt_version

    @fmt_version.setter
    def fmt_version(self, value):
        self._fmt_version = value

    @property
    def port_nic_array(self):
        return self._port_nic_array

    @port_nic_array.setter
    def port_nic_array(self, value):
        self._port_nic_array = value

    def pack(self):
        buf = ""

        # userid=value (string,1-8,char42)
        if len(self._userid) > 0:
            buf += f"userid={self._userid}\x00"

        # vlan_id=value (string,0-8,char42)
        if len(self._vlan_id) > 0:
            buf += f"vlan_id={self._vlan_id}\x00"

        # device=value (string,0-4,char26)
        if len(self._device) > 0:
            buf += f"device={self._device}\x00"

        # fmt_version=value (string,0-10,char10)
        if len(self._fmt_version) > 0:
            buf += f"fmt_version={self._fmt_version}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # port_nic_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._port_nic_array = []
        while alen > 0:
            entry = Obj()
            self._port_nic_array.append(entry)

            # port_nic_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # port_nic_structure
            # pseg_array
            port_nic, \
            _, \
            pseg_array = buf[offset:offset + slen].partition(b"\x00")
            offset += slen

            # type (string,3-4,char26)
            # port_name or nic_addr (string,1-8,char36 plus $#@*)
            # port_nic_num (string,1-10,char10)
            entry.type, \
            port_or_nic, \
            entry.port_nic_num = port_nic.decode("UTF-8").split()

            if entry.type == "PORT":
                entry.port_name = port_or_nic
                entry.nic_addr = ""
            else:
                entry.port_name = ""
                entry.nic_addr = port_or_nic
 
            # port_nic_structure_length (int4)
            slen, = struct.unpack("!I", pseg_array[0:4])

            entry.pseg_array = []
            for ps in pseg_array[4:-1].decode("UTF-8").split("\x00"):
                pseg = Obj()
                entry.pseg_array.append(pseg)

                # pseg_vlanid (string,1-10,char10)
                # pseg_rx (string,1-10,char10)
                # pseg_rx_disc (string,1-10,char10)
                # pseg_tx (string,1-10,char10)
                # pseg_tx_disc (string,1-10,char10)
                pseg.pseg_vlanid, \
                pseg.pseg_rx, \
                pseg.pseg_rx_disc, \
                pseg.pseg_tx, \
                pseg.pseg_tx_disc = ps.split()


