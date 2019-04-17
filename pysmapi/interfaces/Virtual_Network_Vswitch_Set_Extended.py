
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

class Virtual_Network_Vswitch_Set_Extended(Request):
    def __init__(self,
                 switch_name = "",
                 grant_userid = "",
                 user_vlan_id = "",
                 revoke_userid = "",
                 real_device_address = "",
                 port_name = "",
                 controller_name = "",
                 connection_value = "",
                 queue_memory_limit = "",
                 routing_value = "",
                 port_type = "",
                 persist = "",
                 gvrp_value = "",
                 mac_id = "",
                 uplink = "",
                 osd_sim = "",
                 nic_userid = "",
                 nic_vdev = "",
                 lacp = "",
                 interval = "",
                 group_rdev = "",
                 iptimeout = "",
                 port_isolation = "",
                 promiscuous = "",
                 MAC_protect = "",
                 VLAN_counters = "",
                 nic_portselection = "",
                 portnum = "",
                 portnum_modify = "",
                 portnum_remove = "",
                 vlan_port_add = "",
                 vlan_port_remove = "",
                 vlan_delete = "",
                 vepa = "",
                 trace_size = "",
                 ivl_vlanid = "",
                 ivl_heartbeat = "",
                 lacp_group_type = "",
                 **kwargs):
        super(Virtual_Network_Vswitch_Set_Extended, self).__init__(**kwargs)
 
        # Request parameters
        self._switch_name = switch_name
        self._grant_userid = grant_userid
        self._user_vlan_id = user_vlan_id
        self._revoke_userid = revoke_userid
        self._real_device_address = real_device_address
        self._port_name = port_name
        self._controller_name = controller_name
        self._connection_value = connection_value
        self._queue_memory_limit = queue_memory_limit
        self._routing_value = routing_value
        self._port_type = port_type
        self._persist = persist
        self._gvrp_value = gvrp_value
        self._mac_id = mac_id
        self._uplink = uplink
        self._osd_sim = osd_sim
        self._nic_userid = nic_userid
        self._nic_vdev = nic_vdev
        self._lacp = lacp
        self._interval = interval
        self._group_rdev = group_rdev
        self._iptimeout = iptimeout
        self._port_isolation = port_isolation
        self._promiscuous = promiscuous
        self._MAC_protect = MAC_protect
        self._VLAN_counters = VLAN_counters
        self._nic_portselection = nic_portselection
        self._portnum = portnum
        self._portnum_modify = portnum_modify
        self._portnum_remove = portnum_remove
        self._vlan_port_add = vlan_port_add
        self._vlan_port_remove = vlan_port_remove
        self._vlan_delete = vlan_delete
        self._vepa = vepa
        self._trace_size = trace_size
        self._ivl_vlanid = ivl_vlanid
        self._ivl_heartbeat = ivl_heartbeat
        self._lacp_group_type = lacp_group_type

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

    @property
    def grant_userid(self):
        return self._grant_userid

    @grant_userid.setter
    def grant_userid(self, value):
        self._grant_userid = value

    @property
    def user_vlan_id(self):
        return self._user_vlan_id

    @user_vlan_id.setter
    def user_vlan_id(self, value):
        self._user_vlan_id = value

    @property
    def revoke_userid(self):
        return self._revoke_userid

    @revoke_userid.setter
    def revoke_userid(self, value):
        self._revoke_userid = value

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
    def mac_id(self):
        return self._mac_id

    @mac_id.setter
    def mac_id(self, value):
        self._mac_id = value

    @property
    def uplink(self):
        return self._uplink

    @uplink.setter
    def uplink(self, value):
        self._uplink = value

    @property
    def osd_sim(self):
        return self._osd_sim

    @osd_sim.setter
    def osd_sim(self, value):
        self._osd_sim = value

    @property
    def nic_userid(self):
        return self._nic_userid

    @nic_userid.setter
    def nic_userid(self, value):
        self._nic_userid = value

    @property
    def nic_vdev(self):
        return self._nic_vdev

    @nic_vdev.setter
    def nic_vdev(self, value):
        self._nic_vdev = value

    @property
    def lacp(self):
        return self._lacp

    @lacp.setter
    def lacp(self, value):
        self._lacp = value

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def group_rdev(self):
        return self._group_rdev

    @group_rdev.setter
    def group_rdev(self, value):
        self._group_rdev = value

    @property
    def iptimeout(self):
        return self._iptimeout

    @iptimeout.setter
    def iptimeout(self, value):
        self._iptimeout = value

    @property
    def port_isolation(self):
        return self._port_isolation

    @port_isolation.setter
    def port_isolation(self, value):
        self._port_isolation = value

    @property
    def promiscuous(self):
        return self._promiscuous

    @promiscuous.setter
    def promiscuous(self, value):
        self._promiscuous = value

    @property
    def MAC_protect(self):
        return self._MAC_protect

    @MAC_protect.setter
    def MAC_protect(self, value):
        self._MAC_protect = value

    @property
    def VLAN_counters(self):
        return self._VLAN_counters

    @VLAN_counters.setter
    def VLAN_counters(self, value):
        self._VLAN_counters = value

    @property
    def nic_portselection(self):
        return self._nic_portselection

    @nic_portselection.setter
    def nic_portselection(self, value):
        self._nic_portselection = value

    @property
    def portnum(self):
        return self._portnum

    @portnum.setter
    def portnum(self, value):
        self._portnum = value

    @property
    def portnum_modify(self):
        return self._portnum_modify

    @portnum_modify.setter
    def portnum_modify(self, value):
        self._portnum_modify = value

    @property
    def portnum_remove(self):
        return self._portnum_remove

    @portnum_remove.setter
    def portnum_remove(self, value):
        self._portnum_remove = value

    @property
    def vlan_port_add(self):
        return self._vlan_port_add

    @vlan_port_add.setter
    def vlan_port_add(self, value):
        self._vlan_port_add = value

    @property
    def vlan_port_remove(self):
        return self._vlan_port_remove

    @vlan_port_remove.setter
    def vlan_port_remove(self, value):
        self._vlan_port_remove = value

    @property
    def vlan_delete(self):
        return self._vlan_delete

    @vlan_delete.setter
    def vlan_delete(self, value):
        self._vlan_delete = value

    @property
    def vepa(self):
        return self._vepa

    @vepa.setter
    def vepa(self, value):
        self._vepa = value

    @property
    def trace_size(self):
        return self._trace_size

    @trace_size.setter
    def trace_size(self, value):
        self._trace_size = value

    @property
    def ivl_vlanid(self):
        return self._ivl_vlanid

    @ivl_vlanid.setter
    def ivl_vlanid(self, value):
        self._ivl_vlanid = value

    @property
    def ivl_heartbeat(self):
        return self._ivl_heartbeat

    @ivl_heartbeat.setter
    def ivl_heartbeat(self, value):
        self._ivl_heartbeat = value

    @property
    def lacp_group_type(self):
        return self._lacp_group_type

    @lacp_group_type.setter
    def lacp_group_type(self, value):
        self._lacp_group_type = value

    def pack(self):
        buf = ""

        # switch_name=value (string,1-8,char36 plus @#$_)
        buf += f"switch_name={self._switch_name}\x00"

        # grant_userid=value (string,0-8,char42)
        if self._grant_userid:
            buf += f"grant_userid={self._grant_userid}\x00"

        # user_vlan_id=value (string,0-19,char10 plus blank -)
        if self._user_vlan_id:
            buf += f"user_vlan_id={self._user_vlan_id}\x00"

        # revoke_userid=value (string,0-8,char42)
        if self._revoke_userid:
            buf += f"revoke_userid={self._revoke_userid}\x00"

        # real_device_address=value (string,0-23,char16 plus blank . P p)
        if self._real_device_address:
            buf += f"real_device_address={self._real_device_address}\x00"

        # port_name=value (string,0-26,char42 plus blank)
        if self._port_name:
            buf += f"port_name={self._port_name}\x00"

        # controller_name=value (string,0-71,char42 plus blank)
        #                       (string,1,*)
        if self._controller_name:
            buf += f"controller_name={self._controller_name}\x00"

        # connection_value=value (string,0-10,char42)
        if self._connection_value:
            buf += f"connection_value={self._connection_value}\x00"

        # queue_memory_limit=value (string,0-1,char16)
        if self._queue_memory_limit:
            buf += f"queue_memory_limit={self._queue_memory_limit}\x00"

        # routing_value=value (string,0-9,char42)
        if self._routing_value:
            buf += f"routing_value={self._routing_value}\x00"

        # port_type=value (string,0-6,char42)
        if self._port_type:
            buf += f"port_type={self._port_type}\x00"

        # persist=value (string,0-3,char42)
        if self._persist:
            buf += f"persist={self._persist}\x00"

        # gvrp_value=value (string,0-6,char42)
        if self._gvrp_value:
            buf += f"gvrp_value={self._gvrp_value}\x00"

        # mac_id=value (string,0-6,char16)
        if self._mac_id:
            buf += f"mac_id={self._mac_id}\x00"

        # uplink=value (string,0-3,char42)
        if self._uplink:
            buf += f"uplink={self._uplink}\x00"

        # osd_sim=value (string,0-3,char42)
        if self._osd_sim:
            buf += f"osd_sim={self._osd_sim}\x00"

        # nic_userid=value (string,0-8,char42)
        #                  (string,1,*)
        if self._nic_userid:
            buf += f"nic_userid={self._nic_userid}\x00"

        # nic_vdev=value (string,0-4,char16)
        if self._nic_vdev:
            buf += f"nic_vdev={self._nic_vdev}\x00"

        # lacp=value (string,0-8,char42)
        if self._lacp:
            buf += f"lacp={self._lacp}\x00"

        # interval=value (string,0-8,char42)
        if self._interval:
            buf += f"interval={self._interval}\x00"

        # group_rdev=value (string,0-63,char16 plus blank . P p)
        if self._group_rdev:
            buf += f"group_rdev={self._group_rdev}\x00"

        # iptimeout=value (string,0-3,char10)
        if self._iptimeout:
            buf += f"iptimeout={self._iptimeout}\x00"

        # port_isolation=value (string,0-3,char26)
        if self._port_isolation:
            buf += f"port_isolation={self._port_isolation}\x00"

        # promiscuous=value (string,0-3,char26)
        if self._promiscuous:
            buf += f"promiscuous={self._promiscuous}\x00"

        # MAC_protect=value (string,0-11,char26)
        if self._MAC_protect:
            buf += f"MAC_protect={self._MAC_protect}\x00"

        # VLAN_counters=value (string,0-3,char26)
        if self._VLAN_counters:
            buf += f"VLAN_counters={self._VLAN_counters}\x00"

        # nic_portselection=value (string,0-7,char26)
        if self._nic_portselection:
            buf += f"nic_portselection={self._nic_portselection}\x00"

        # portnum=value (string,0-16,char42 plus blank)
        if self._portnum:
            buf += f"portnum={self._portnum}\x00"

        # portnum_modify=value (string,0-16,char16)
        if self._portnum_modify:
            buf += f"portnum_modify={self._portnum_modify}\x00"

        # portnum_remove=value (string,0-16,char16)
        if self._portnum_remove:
            buf += f"portnum_remove={self._portnum_remove}\x00"

        # vlan_port_add=value (string,0-maxlength,char42 plus blank)
        if self._vlan_port_add:
            buf += f"vlan_port_add={self._vlan_port_add}\x00"

        # vlan_port_remove=value (string,0-maxlength,char42 plus blank)
        if self._vlan_port_remove:
            buf += f"vlan_port_remove={self._vlan_port_remove}\x00"

        # vlan_delete=value (string,0-8,char42)
        if self._vlan_delete:
            buf += f"vlan_delete={self._vlan_delete}\x00"

        # vepa=value (string,0-3,char26)
        if self._vepa:
            buf += f"vepa={self._vepa}\x00"

        # trace_size=value (string,0-4,char10; range 0-4095)
        if self._trace_size:
            buf += f"trace_size={self._trace_size}\x00"

        # ivl_vlanid=value (string,0-4,char10; range 1-4094)
        if self._ivl_vlanid:
            buf += f"ivl_vlanid={self._ivl_vlanid}\x00"

        # ivl_heartbeat=value (string,0-4,char10; range 10-3600)
        if self._ivl_heartbeat:
            buf += f"ivl_heartbeat={self._ivl_heartbeat}\x00"

        # lacp_group_type=value (string,0-9,char42)
        if self._lacp_group_type:
            buf += f"lacp_group_type={self._lacp_group_type}\x00"

        return s2b(buf)

