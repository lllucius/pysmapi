
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

class Virtual_Network_Vswitch_Query(Request):
    # Port type
    ACCESS = 1
    TRUNK = 2
    port_type_names = {ACCESS: "ACCESS", TRUNK: "TRUNK"}

    # Transport type
    IP = 1
    ETHERNET = 2
    transport_type_names = {IP: "IP", ETHERNET: "ETHERNET"}

    # Routing value
    NONROUTER = 1
    PRIROUTER = 2
    routing_value_names = {NONROUTER: "NONROUTER", PRIROUTER: "PRIROUTER"}

    # VLAN id
    NOTSPECIFIED = -1
    UNAWARE = 0
    vlan_id_names = {NOTSPECIFIED: "NOTSPECIFIED", UNAWARE: "UNAWARE"}

    # GVRP request attribute
    REQUESTED = 1
    NOTREQUESTED = 2
    gvrp_request_attribute_names = {REQUESTED: "REQUESTED", NOTREQUESTED: "NOTREQUESTED"}

    # GVRP enabled attribute
    GVRP_ENABLED = 1
    GVRP_NOT_ENABLED = 2
    gvrp_enabled_attribute_names = {GVRP_ENABLED: "ENABLED", GVRP_ENABLED: "NOTENABLED"}

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
    
    def __init__(self,
                 switch_name = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Query, self).__init__(**kwargs)

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
        sn_len = len(self._switch_name)

        # switch_name_length (int4)
        # switch_name (string,1-8,char36 plus @#$_)
        fmt = "!I%ds" % (sn_len)
  
        buf = struct.pack(fmt,
                          sn_len,
                          s2b(self._switch_name))

        return buf

    def unpack(self, buf):
        offset = 0

        # vswitch_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._vswitch_array = []
        while alen > 0:
            entry = Obj()
            self._vswitch_array.append(entry)

            # vswitch_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # switch_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # switch_name (string,1-8,char36 plus $#@)
            entry.switch_name = b2s(buf[offset:offset + nlen])
            offset += nlen

            # transport_type (int1)
            # port_type (int1)
            # queue_memory_limit (int4)
            # routing_value (int1)
            # vlan_id (int4)
            # native_vlan_id (int4)
            # mac_id (int8)
            # gvrp_request_attribute (int1)
            # gvrp_enabled_attribute (int1)
            # switch_status (int1)
            entry.transport_type, \
            entry.port_type, \
            entry.queue_memory_limit, \
            entry.routing_value, \
            entry.vlan_id, \
            entry.native_vlan_id, \
            entry.mac_id, \
            entry.gvrp_request_attribute, \
            entry.gvrp_enabled_attribute, \
            entry.switch_status = struct.unpack("!BBIBIIQBBB", buf[offset:offset + 26])
            offset += 26

            # real_device_array_length (int4)
            dlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            entry.real_device_array = []
            while dlen > 0:
                device = Obj()
                entry.real_device_array.append(device)

                # real_device_structure_length (int4)
                slen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4
                dlen -= (slen + 4)

                # real_device_address (int4)
                device.real_device_address, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # controller_name_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # controller_name (string,0-71,char42 plus blank)
                device.controller_name = b2s(buf[offset:offset + nlen])
                offset += nlen

                # port_name_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # port_name (string,0-16,char16)
                device.port_name = b2s(buf[offset:offset + nlen])
                offset += nlen

                # device_status (int1)
                # device_error_status (int1)
                device.device_status = \
                device.device_error_status = 0

                device.device_status, \
                device.device_error_status = struct.unpack("!BB", buf[offset:offset + 2])
                offset += 2

            # authorized_user_array_length (int4)
            dlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            entry.authorized_user_array = []
            while dlen > 0:
                user = Obj()
                entry.authorized_user_array.append(user)

                # authorized_user_structure_length (int4)
                slen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4
                dlen -= (slen + 4)

                # grant_userid_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # grant_userid (string,1-8.char42)
                user.grant_userid = b2s(buf[offset:offset + nlen])
                offset += nlen

                # vlan_array_length (int4)
                vlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                user.vlan_array = []
                while vlen > 0:
                    vlan = Obj()
                    user.vlan_array.append(vlan)

                    # vlan_structure_length (int4)
                    slen, = struct.unpack("!I", buf[offset:offset + 4])
                    offset += 4
                    vlen -= (slen + 4)

                    # user_vlan_id (int4)
                    vlan.user_vlan_id, = struct.unpack("!I", buf[offset:offset + 4])
                    offset += 4

            # connected_adapter_array_length (int4)
            dlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            entry.connected_adapter_array = []
            while dlen > 0:
                adapter = Obj()
                entry.connected_adapter_array.append(adapter)

                # connected_adapter_structure_length (int4)
                slen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4
                dlen -= (slen + 4)

                # adapter_owner_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # adapter_owner (string,1-8,char42)
                adapter.adapter_owner = b2s(buf[offset:offset + nlen])
                offset += nlen

                # image_device_number_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # image_device_number (string,1-4,char16)
                adapter.image_device_number = b2s(buf[offset:offset + nlen])
                offset += nlen

