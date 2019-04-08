
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

from pysmapi.smapi import Request, Obj

class Virtual_Network_Vswitch_Query_Stats(Request):
    def __init__(self,
                 switch_name = "",
                 fmt_version = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Query_Stats, self).__init__(**kwargs)

        # Request parameters
        self._switch_name = switch_name
        self._fmt_version = fmt_version

        # Response values
        self._vswitch_array = []

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def fmt_version(self):
        return self._fmt_version

    @fmt_version.setter
    def fmt_version(self, value):
        self._fmt_version = value

    @property
    def vswitch_array(self):
        return self._vswitch_array

    @vswitch_array.setter
    def vswitch_array(self, value):
        self._vswitch_array = value

    def pack(self):
        buf = ""

        # switch_name=value (string,1-8,char36 plus @#$_)
        buf += f"switch_name={self._switch_name}\x00"

        # fmt_version=value (string,0-10,char10)
        if len(self._fmt_version) > 0:
            buf += f"fmt_version={self._fmt_version}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # vswitch_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._vswitch_array = []
        while alen > 0:
            vswitch = Obj()
            self._vswitch_array.append(vswitch)

            # switch_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= 4

            # switch_name (string,0-8,char36 plus $#@)
            vswitch.switch_name = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen
            alen -= nlen

            # segment_array_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            vswitch.segment_array = []
            for items in buf[offset:offset + slen - 1].decode("UTF-8").split("\x00"):
                segment = Obj()
                vswitch.segment_array.append(segment)

                # seg_vlanid (string,1-10,char10)
                # seg_rx (string,1-10,char10)
                # seg_rx_disc (string,1-10,char10)
                # seg_tx (string,1-10,char10)
                # seg_tx_disc (string,1-10,char10)
                # seg_activated_TOD (string,1-10,char10 plus *)
                # seg_config_update_TOD (string,1-10,char10 plus *)
                # seg_vlan_interfaces (string,1-10,char10 plus *)
                # seg_vlan_deletes (string,1-10,char10)
                # seg_device_type (string,4,char26)
                # seg_device_addr (string,4,char16)
                # seg_device_status (string,1,char10)
                segment.seg_vlanid, \
                segment.seg_rx, \
                segment.seg_rx_disc, \
                segment.seg_tx, \
                segment.seg_tx_disc, \
                segment.seg_activated_TOD, \
                segment.seg_config_update_TOD, \
                segment.seg_vlan_interfaces, \
                segment.seg_vlan_deletes, \
                segment.seg_device_type, \
                segment.seg_device_addr, \
                segment.seg_device_status = items.split()

