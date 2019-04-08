
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

class Virtual_Network_Vswitch_Query(Request):
    # Connection value
    UNSPECIFIED = 0
    ACTIVATE = 1
    NOACTIVATE = 2

    # Routing value
    NONROUTER = 1
    PRIROUTER = 2
    routing_value_names = ["?", "NONROUTER", "ROUTER"]

    # Transport type
    IP = 1
    ETHERNET = 2
    transport_type_names = ["?", "IP", "ETHERNET"]

    # VLAN id
    NOTSPECIFIED = -1
    UNAWARE = 0

    # Port type
    ACCESS = 1
    TRUNK = 2
    port_type_names = ["?", "ACCESS", "TRUNK"]

    # GVRP request attribute
    REQUESTED = 1
    NOTREQUESTED = 2
    gvrp_request_attribute_names = ["?", "REQUESTED", "NOTREQUESTED"]

    # GVRP enabled attribute
    GVRP_ENABLED = 1
    GVRP_NOT_ENABLED = 2
    gvrp_enabled_attribute_names = ["?", "ENABLED", "NOTENABLED"]

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
        ["virtual switch defined",
         "controller not available",
         "operator intervention required",
         "disconnected",
         "virtual devices attached to controller",
         "OSA initialization in progress",
         "OSA device not ready",
         "OSA device ready",
         "OSA devices being detached",
         "virtual switch delete pending",
         "virtual switch failover recovering",
         "autorestart in progress"]

    # Device status
    NOT_ACTIVE = 0
    ACTIVE = 1
    BACKUP = 2
    device_status_names = ["NOT ACTIVE", "ACTIVE", "BACKUP"]

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
        ["No error",
         "Port name conflict",
         "No layer 2 support",
         "Real device does not exist",
         "Real device is attached elsewhere",
         "Real device is not compatible type",
         "Initialization error",
         "Stalled OSA",
         "Stalled controller",
         "Controller connection severed",
         "Primary or secondary routing conflict",
         "Device is offline",
         "Device was detached",
         "IP/Ethernet type mismatch",
         "Insufficient memory in controller virtual machine",
         "TCP/IP configuration conflict",
         "No link aggregation support",
         "OSA-E attribute mismatch",
         "Reserved for future use",
         "OSA-E is not ready",
         "Reserved for future use",
         "Attempting restart for device",
         "Exclusive user error",
         "Device state is invalid",
         "Port number is invalid for device",
         "No OSA connection isolation",
         "EQID mismatch",
         "Incompatible controller",
         "BACKUP detached",
         "BACKUP not ready",
         "BACKUP attempting restart",
         "EQID mismatch",
         "No HiperSockets bridge support",
         "HiperSockets bridge error"]
    
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
                          bytes(self._switch_name, "UTF-8"))

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
            entry.switch_name = buf[offset:offset + nlen].decode("UTF-8")
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
                device.controller_name = buf[offset:offset + nlen].decode("UTF-8")
                offset += nlen

                # port_name_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # port_name (string,0-16,char16)
                device.port_name = buf[offset:offset + nlen].decode("UTF-8")
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
                user.grant_userid = buf[offset:offset + nlen].decode("UTF-8")
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
                adapter.adapter_owner = buf[offset:offset + nlen].decode("UTF-8")
                offset += nlen

                # image_device_number_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # image_device_number (string,1-4,char16)
                adapter.image_device_number = buf[offset:offset + nlen].decode("UTF-8")
                offset += nlen

