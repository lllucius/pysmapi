
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

class Virtual_Network_Vswitch_Create(Request):
    # (shared)
    UNSPECIFIED = 0

    # Connection value
    ACTIVATE = 1
    NOACTIVATE = 2

    # Routing value
    NONROUTER = 1
    PRIROUTER = 2

    # Transport type
    IP = 1
    ETHERNET = 2

    # VLAN id
    NOTSPECIFIED = -1
    UNAWARE = 0

    # Port type
    ACCESS = 1
    TRUNK = 2

    # Update system config indicator    
    CREATE = 1
    CREATEADD = 2
    ADD = 3

    # GVRP value
    GVRP = 1
    NOGVRP = 2

    def __init__(self,
                 switch_name = "",
                 real_device_address = "",
                 port_name = "",
                 controller_name = "",
                 connection_value = UNSPECIFIED,
                 queue_memory_limit = 0,
                 routing_value = UNSPECIFIED,
                 transport_type = UNSPECIFIED,
                 vlan_id = NOTSPECIFIED,
                 port_type = UNSPECIFIED,
                 update_system_config_indicator = UNSPECIFIED,
                 system_config_name = "",
                 system_config_type = "",
                 parm_disk_owner = "",
                 parm_disk_number = "",
                 parm_disk_password = "",
                 alt_system_config_name = "",
                 alt_system_config_type = "",
                 alt_parm_disk_owner = "",
                 alt_parm_disk_number = "",
                 alt_parm_disk_password = "",
                 gvrp_value = UNSPECIFIED,
                 native_vlanid = NOTSPECIFIED,                 
                 **kwargs):
        super(Virtual_Network_Vswitch_Create, self).__init__(**kwargs)

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
        self._update_system_config_indicator = update_system_config_indicator
        self._system_config_name = system_config_name
        self._system_config_type = system_config_type
        self._parm_disk_owner = parm_disk_owner
        self._parm_disk_number = parm_disk_number
        self._parm_disk_password = parm_disk_password
        self._alt_system_config_name = alt_system_config_name
        self._alt_system_config_type = alt_system_config_type
        self._alt_parm_disk_owner = alt_parm_disk_owner
        self._alt_parm_disk_number = alt_parm_disk_number
        self._alt_parm_disk_password = alt_parm_disk_password
        self._gvrp_value = gvrp_value
        self._native_vlanid = native_vlanid

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
    def update_system_config_indicator(self):
        return self._update_system_config_indicator

    @update_system_config_indicator.setter
    def update_system_config_indicator(self, value):
        self._update_system_config_indicator = value

    @property
    def system_config_name(self):
        return self._system_config_name

    @system_config_name.setter
    def system_config_name(self, value):
        self._system_config_name = value

    @property
    def system_config_type(self):
        return self._system_config_type

    @system_config_type.setter
    def system_config_type(self, value):
        self._system_config_type = value

    @property
    def parm_disk_owner(self):
        return self._parm_disk_owner

    @parm_disk_owner.setter
    def parm_disk_owner(self, value):
        self._parm_disk_owner = value

    @property
    def parm_disk_number(self):
        return self._parm_disk_number

    @parm_disk_number.setter
    def parm_disk_number(self, value):
        self._parm_disk_number = value

    @property
    def parm_disk_password(self):
        return self._parm_disk_password

    @parm_disk_password.setter
    def parm_disk_password(self, value):
        self._parm_disk_password = value

    @property
    def alt_system_config_name(self):
        return self._alt_system_config_name

    @alt_system_config_name.setter
    def alt_system_config_name(self, value):
        self._alt_system_config_name = value

    @property
    def alt_system_config_type(self):
        return self._alt_system_config_type

    @alt_system_config_type.setter
    def alt_system_config_type(self, value):
        self._alt_system_config_type = value

    @property
    def alt_parm_disk_owner(self):
        return self._alt_parm_disk_owner

    @alt_parm_disk_owner.setter
    def alt_parm_disk_owner(self, value):
        self._alt_parm_disk_owner = value

    @property
    def alt_parm_disk_number(self):
        return self._alt_parm_disk_number

    @alt_parm_disk_number.setter
    def alt_parm_disk_number(self, value):
        self._alt_parm_disk_number = value

    @property
    def alt_parm_disk_password(self):
        return self._alt_parm_disk_password

    @alt_parm_disk_password.setter
    def alt_parm_disk_password(self, value):
        self._alt_parm_disk_password = value

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

    def pack(self):
        sn_len = len(self._switch_name)
        rda_len = len(self._real_device_address)
        pn_len = len(self._port_name)
        cn_len = len(self._controller_name)
        scn_len = len(self._system_config_name)
        sct_len = len(self._system_config_type)
        pdo_len = len(self._parm_disk_owner)
        pdn_len = len(self._parm_disk_number)
        pdp_len = len(self._parm_disk_password)
        ascn_len = len(self._alt_system_config_name)
        asct_len = len(self._alt_system_config_type)
        apdo_len = len(self._alt_parm_disk_owner)
        apdn_len = len(self._alt_parm_disk_number)
        apdp_len = len(self._alt_parm_disk_password)

        # switch_name_length (int4)
        # switch_name (string,1-8,char36 plus @#$_)
        # real_device_address_length (int4)
        # real_device_address (string,0-14,char16 plus blank)
        # port_name_length (int4)
        # port_name (string,0-26,char42 plus blank)
        # controller_name_length (int4)
        # controller_name (string,0-8,char42)
        #                 (string,1,*)
        # connection_value (int1)
        # queue_memory_limit (int4)
        # routing_value (int1)
        # transport_type (int1)
        # vlan_id (int4)
        # port_type (int1)
        # update_system_config_indicator (int1)
        # system_config_name_length (int4)
        # system_config_name (string,0-8,char42)
        # system_config_type_length (int4)
        # system_config_type (string,0-8,char42)
        # parm_disk_owner_length (int4)
        # parm_disk_owner (string,0-8,char42)
        # parm_disk_number_length (int4)
        # parm_disk_number (string,0-4,char16)
        # parm_disk_password_length (int4)
        # parm_disk_password (string,0-8,charNB)
        # alt_system_config_name_length (int4)
        # alt_system_config_name (string,0-8,char42)
        # alt_system_config_type_length (int4)
        # alt_system_config_type (string,0-8,char42)
        # alt_parm_disk_owner_length (int4)
        # alt_parm_disk_owner (string,0-8,char42)
        # alt_parm_disk_number_length (int4)
        # alt_parm_disk_number (string,0-4,char16)
        # alt_parm_disk_password_length (int4)
        # alt_parm_disk_password (string,0-8,charNB)
        # gvrp_value (int1)
        # native_vlanid (int4)
        fmt = "!I%dsI%dsI%dsI%dsBIBBiBBI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsBi" % \
            (sn_len,
             rda_len,
             pn_len,
             cn_len,
             scn_len,
             sct_len,
             pdo_len,
             pdn_len,
             pdp_len,
             ascn_len,
             asct_len,
             apdo_len,
             apdn_len,
             apdp_len)
 
        buf = struct.pack(fmt,
                          sn_len,
                          s2b(self._switch_name),
                          rda_len,
                          s2b(self._real_device_address),
                          pn_len,
                          s2b(self._port_name),
                          cn_len,
                          s2b(self._controller_name),
                          self._connection_value,
                          self._queue_memory_limit,
                          self._routing_value,
                          self._transport_type,
                          self._vlan_id,
                          self._port_type,
                          self._update_system_config_indicator,
                          scn_len,
                          s2b(self._system_config_name),
                          sct_len,
                          s2b(self._system_config_type),
                          pdo_len,
                          s2b(self._parm_disk_owner),
                          pdn_len,
                          s2b(self._parm_disk_number),
                          pdp_len,
                          s2b(self._parm_disk_password),
                          ascn_len,
                          s2b(self._alt_system_config_name),
                          asct_len,
                          s2b(self._alt_system_config_type),
                          apdo_len,
                          s2b(self._alt_parm_disk_owner),
                          apdn_len,
                          s2b(self._alt_parm_disk_number),
                          apdp_len,
                          s2b(self._alt_parm_disk_password),
                          self._gvrp_value,
                          self._native_vlanid)

        return buf
