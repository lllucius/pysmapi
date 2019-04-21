
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

class Virtual_Network_Vswitch_Query_Extended(Request):
    # Switch status
    SWITCH_DEFINED = 1
    CONTROLLER_NOT_AVAILABLE = 2
    OPERATOR_INTERVENTION_REQUIRED = 3
    DISCONNECTED = 4
    DEVICES_ATTACHED = 5
    OSA_INITIALIZING = 6
    OSA_NOT_READY = 7
    OSA_READY = 8
    OSA_DETACHING = 9
    DELETE_PENDING = 10
    RECOVERING = 11
    RESTARTING = 12
    switch_status_names = \
        {SWITCH_DEFINED: "virtual switch defined",
         CONTROLLER_NOT_AVAILABLE: "controller not available",
         OPERATOR_INTERVENTION_REQUIRED: "operator intervention required",
         DISCONNECTED: "disconnected",
         DEVICES_ATTACHED: "virtual devices attached to controller",
         OSA_INITIALIZING: "OSA initialization in progress",
         OSA_NOT_READY: "OSA device not ready",
         OSA_READY: "OSA device ready",
         OSA_DETACHING: "OSA devices being detached",
         DELETE_PENDING: "virtual switch delete pending",
         RECOVERING: "virtual switch failover recovering",
         RESTARTING: "autorestart in progress"}

    # Device status
    NOT_ACTIVE = 0
    ACTIVE = 1
    BACKUP = 2
    device_status_names = {NOT_ACTIVE: "NOT ACTIVE", ACTIVE: "ACTIVE", BACKUP: "BACKUP"}

    # Device error status
    NO_ERROR = 0
    PORT_NAME_CONFLICT = 1
    NO_LAYER2_SUPPORT = 2
    DEVICE_NOT_FOUND = 3
    DEVICE_IN_USE = 4
    DEVICE_NOT_COMPATIBLE = 5
    INITIALIZATION_ERROR = 6
    STALLED_OSA = 7
    STALLED_CONTROLLER = 8
    CONNECTION_SEVERED = 9
    ROUTING_CONFLICT = 10
    DEVICE_OFFLINE = 11
    DEVICE_DETACHED = 12
    TRANSPORT_TYPE_MISMATCH = 13
    INSUFFICIENT_MEMORY = 14
    TCPIP_CONFIGURATION_CONFLICT = 15
    NO_LINK_AGGREGRATION_SUPPORT = 16
    OSAE_ATTRIBUTE_MISMATCH = 17
    RESERVED18 = 18
    OSAE_NOT_READY = 19
    RESERVED20 = 20
    ATTEMPTING_RESTART = 21
    EXCLUSIVE_USER_ERROR = 22
    DEVICE_STATE_INVALID = 23
    PORT_NUMBER_INVALID = 24
    NO_ISOLATION = 25
    EQID_MISMATCH = 26
    INCOMPATIBLE_CONTROLLER = 27
    BACKUP_DETACHED = 28
    BACKUP_NOT_READY = 29
    BACKUP_RESTARTING = 30
    EQID_MISMATCH31 = 31
    NO_HIPERSOCKETS_BRIDGE_SUPPORT = 32
    HIPERSOCKETS_BRIDGE_ERROR = 33
    device_error_status_names = \
        {NO_ERROR: "No error",
         PORT_NAME_CONFLICT: "Port name conflict",
         NO_LAYER2_SUPPORT: "No layer 2 support",
         DEVICE_NOT_FOUND: "Real device does not exist",
         DEVICE_IN_USE: "Real device is attached elsewhere",
         DEVICE_NOT_COMPATIBLE: "Real device is not compatible type",
         INITIALIZATION_ERROR: "Initialization error",
         STALLED_OSA: "Stalled OSA",
         STALLED_CONTROLLER: "Stalled controller",
         CONNECTION_SEVERED: "Controller connection severed",
         ROUTING_CONFLICT: "Primary or secondary routing conflict",
         DEVICE_OFFLINE: "Device is offline",
         DEVICE_DETACHED: "Device was detached",
         TRANSPORT_TYPE_MISMATCH: "IP/Ethernet type mismatch",
         INSUFFICIENT_MEMORY: "Insufficient memory in controller virtual machine",
         TCPIP_CONFIGURATION_CONFLICT: "TCP/IP configuration conflict",
         NO_LINK_AGGREGRATION_SUPPORT: "No link aggregation support",
         OSAE_ATTRIBUTE_MISMATCH: "OSA-E attribute mismatch",
         RESERVED18: "Reserved for future use",
         OSAE_NOT_READY: "OSA-E is not ready",
         RESERVED20: "Reserved for future use",
         ATTEMPTING_RESTART: "Attempting restart for device",
         EXCLUSIVE_USER_ERROR: "Exclusive user error",
         DEVICE_STATE_INVALID: "Device state is invalid",
         PORT_NUMBER_INVALID: "Port number is invalid for device",
         NO_ISOLATION: "No OSA connection isolation",
         EQID_MISMATCH: "EQID mismatch",
         INCOMPATIBLE_CONTROLLER: "Incompatible controller",
         BACKUP_DETACHED: "BACKUP detached",
         BACKUP_NOT_READY: "BACKUP not ready",
         BACKUP_RESTARTING: "BACKUP attempting restart",
         EQID_MISMATCH31: "EQID mismatch",
         NO_HIPERSOCKETS_BRIDGE_SUPPORT: "No HiperSockets bridge support",
         HIPERSOCKETS_BRIDGE_ERROR: "HiperSockets bridge error"}

    # Uplink NIC error status
    NO_ERROR = 0
    USERID_NOT_LOGGED_ON = 1
    NOT_AUTHORIZED = 2
    VDEV_DOES_NOT_EXIST = 3
    VDEV_IN_USE = 4 
    VDEV_NOT_COMPATIBLE = 5
    VLAN_CONFLICT = 6
    NO_MAC_ADDRESS = 7
    NOT_MANAGED = 8
    PORT_ERROR = 9
    TYPE_MISMATCH = 13
    UNKNOWN_ERROR = 255 
    uplink_NIC_error_status_names = \
        {NO_ERROR: "No error",
         USERID_NOT_LOGGED_ON: "Userid not logged on",
         NOT_AUTHORIZED: "Not authorized",
         VDEV_DOES_NOT_EXIST: "VDEV does not exist",
         VDEV_IN_USE: "VDEV is attached elsewhere",
         VDEV_NOT_COMPATIBLE: "VDEV not compatible type",
         VLAN_CONFLICT: "VLAN conflict",
         NO_MAC_ADDRESS: "No MAC address",
         NOT_MANAGED: "Not managed",
         PORT_ERROR: "Port Error",
         TYPE_MISMATCH: "Type mismatch",
         UNKNOWN_ERROR: "Unknown error"}
             
    def __init__(self,
                 switch_name = "",
                 vepa_status = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Query_Extended, self).__init__(**kwargs)

        # Request parameters
        self._switch_name = switch_name
        self._vepa_status = vepa_status

        # Response values
        self._vswitch_array = []

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def vepa_status(self):
        return self._vepa_status

    @vepa_status.setter
    def vepa_status(self, value):
        self._vepa_status = value

    @property
    def vswitch_array(self):
        return self._vswitch_array

    @vswitch_array.setter
    def vswitch_array(self, value):
        self._vswitch_array = value

    def pack(self):
        buf = ""

        # switch_name=value (string,1-8,char36 plus @#$_)
        #                   (string,1,*)
        buf += f"switch_name={self._switch_name}\x00"

        # vepa_status=value (string,2-3,char26)  
        buf += f"vepa_status={self._vepa_status}\x00"

        return s2b(buf)

    def unpack(self, buf):
        offset = 0

        # vswitch_count (int4)
        count, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._vswitch_array = []
        while count > 0:
            count -= 1

            vswitch = Obj()
            self._vswitch_array.append(vswitch)

            # vswitch_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # vswitch_attr_info_structure_length (int4)
            ilen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # switch_name (string,1-8,char36 plus @#$_)
            # transport_type (string,2-8,char26)
            # port_type (string,4-6,char26)
            # queue_memory_limit (string,1-3,char10)
            # routing_value (string,2-9,char26)
            # vlan_awareness (string,5-7,char26)
            # vlan_id (string,1-8,char42)
            # native_vlan_id (string,1-8,char42)
            # mac_address (string,17,char16 plus -)
            # gvrp_request_attribute (string,4-6,char26)
            # gvrp_enabled_attribute (string,4-6,char26)
            # switch_status (string,1-2,char10)
            # link_ag (string,4-41,char26)
            # lag_interval (string.1-3,char10)
            # lag_group (string,1-8,char42)
            # IP_timeout (string.1-3,char10)
            # switch_type (string,4,char26)
            # isolation_status (string,9-11,char26)
            # MAC_protect (string,10-13,char26)
            # user_port_based (string,9,char26)
            # VLAN_counters (string,8-10,char26)
            # vepa_status (string,2-3,char26)
            # spg_scope (string,5-7,char26)
            vswitch.switch_name, \
            vswitch.transport_type, \
            vswitch.port_type, \
            vswitch.queue_memory_limit, \
            vswitch.routing_value, \
            vswitch.vlan_awareness, \
            vswitch.vlan_id, \
            vswitch.native_vlan_id, \
            vswitch.mac_address, \
            vswitch.gvrp_request_attribute, \
            vswitch.gvrp_enabled_attribute, \
            vswitch.switch_status, \
            vswitch.link_ag, \
            vswitch.lag_interval, \
            vswitch.lag_group, \
            vswitch.IP_timeout, \
            vswitch.switch_type, \
            vswitch.isolation_status, \
            vswitch.MAC_protect, \
            vswitch.user_port_based, \
            vswitch.VLAN_counters, \
            vswitch.vepa_status, \
            vswitch.spg_scope = b2s(buf[offset:offset + ilen - 1]).split()
            offset += ilen

            # real_device_info_array_length (int4)
            ilen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            vswitch.real_device_info_array = []
            if ilen:
                array = b2s(buf[offset:offset + ilen - 1]).split("\x00")
                offset += ilen

                for item in array:
                    device = Obj()
                    vswitch.real_device_info_array.append(device)

                    # real_device_address (string,4,char16)
                    # virtual_device_address (string,4,char16)
                    # controller_name (string,1-71,char42 plus _)
                    # port_name (string,1-8,char42)
                    # device_status (string,1,char10)
                    # device_error_status (string,1-2,char10)
                    device.real_device_address, \
                    device.virtual_device_address, \
                    device.controller_name, \
                    device.port_name, \
                    device.device_status, \
                    device.device_error_status = item.split()

            # authorized_user_array_length (int4)
            ilen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            vswitch.authorized_user_array = []
            if ilen:
                array = b2s(buf[offset:offset + ilen - 1]).split("\x00")
                offset += ilen

                for item in array:
                    user = Obj()
                    vswitch.authorized_user_array.append(user)

                    item = item.split()

                    # port_num (string,1-16,char16)
                    # grant_userid (string,1-8,char42)
                    # promiscuous_mode (string,4-6,char26)
                    # osd_sim (string,6-8,char26)
                    # vlan_count (string,1-2,char10)
                    user.port_num, \
                    user.grant_userid, \
                    user.promiscuous_mode, \
                    user.osd_sim, \
                    vlan_count = item[:5]

                    user.vlan_array = []
                    for vlanid in item[5:]:
                        vlan = Obj()
                        user.vlan_array.append(vlan)

                        # user_vlan_id (string,1-8,char42)
                        vlan.user_vlan_id = vlanid

            # connected_adapter_array_length (int4)
            ilen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            vswitch.connected_adapter_array = []
            if ilen:
                array = b2s(buf[offset:offset + ilen - 1]).split("\x00")
                offset += ilen

                for item in array:
                    adapter = Obj()
                    vswitch.connected_adapter_array.append(adapter)

                    # adapter_owner (string,1-8,char42)
                    # adapter_vdev (string,4,char16)
                    # adapter_macaddr (string,6-17,char36)
                    # adapter_type (string,4-12,char26)
                    adapter.adapter_owner, \
                    adapter.adapter_vdev, \
                    adapter.adapter_macaddr, \
                    adapter.adapter_type = item.split()

            # uplink_NIC_structure_length (int4)
            ilen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            vswitch.uplink_structure = []
            if ilen:
                array = b2s(buf[offset:offset + ilen - 1]).split("\x00")
                offset += ilen

                for item in array:
                    uplink = Obj()
                    vswitch.uplink_structure.append(uplink)

                    # uplink_NIC_userid (string,1-8,char42)
                    # uplink_NIC_vdev (string,4,char16)
                    # uplink_NIC_error_status (string,1-3,char10)
                    uplink.uplink_NIC_userid, \
                    uplink.uplink_NIC_vdev, \
                    uplink.uplink_NIC_error_status = item.split()

            # global_member_array_length (int4)
            ilen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            vswitch.global_member_array = []
            if ilen:
                array = b2s(buf[offset:offset + ilen - 1]).split("\x00")
                offset += ilen

                for item in array:
                    member = Obj()
                    vswitch.global_member_array.append(device)

                    # member_name (string,1-8,char36 plus @#$_)
                    # member_state (string,5-7,char26)
                    member.member_name, \
                    member.member_state = item.split()
