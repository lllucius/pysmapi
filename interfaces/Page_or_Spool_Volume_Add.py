
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

from base import Smapi_Request_Base, Obj

class Page_or_Spool_Volume_Add(Smapi_Request_Base):
    def __init__(self,
                 vol_addr = 0,
                 volume_label = b"",
                 volume_use = b"",
                 system_config_name = b"",
                 system_config_type = b"",
                 parm_disk_owner = b"",
                 parm_disk_number = b"",
                 parm_disk_password = b"",
                 **kwargs):
        super(Page_or_Spool_Volume_Add, self). \
            __init__(b"Page_or_Spool_Volume_Add", **kwargs)

        # Request parameters
        self._vol_addr = vol_addr
        self._volume_label = volume_label
        self._volume_use = volume_use
        self._system_config_name = system_config_name
        self._system_config_type = system_config_type
        self._parm_disk_owner = parm_disk_owner
        self._parm_disk_number = parm_disk_number
        self._parm_disk_password = parm_disk_password

    @property
    def vol_addr(self):
        return self._vol_addr

    @vol_addr.setter
    def vol_addr(self, value):
        self._vol_addr = value

    @property
    def volume_label(self):
        return self._volume_label

    @volume_label.setter
    def volume_label(self, value):
        self._volume_label = value

    @property
    def volume_use(self):
        return self._volume_use

    @volume_use.setter
    def volume_use(self, value):
        self._volume_use = value

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

    def pack(self):
        buf = b""

        # vol_addr=value (string,1-4,char16)
        buf += b"vol_addr=%s\x00" % (self._vol_addr)

        # volume_label=value (string,1-6,char36)
        buf += b"volume_label=%s\x00" % (self._volume_label)

        # volume_use=value (string,4-5,char26)
        buf += b"volume_use=%s\x00" % (self._volume_use)

        # system_config_name (string,0-8,char42)
        if len(self._system_config_name) > 0:
            buf += b"system_config_name=%s\x00" % (self._system_config_name)

        # system_config_type (string,0-8,char42)
        if len(self._system_config_type) > 0:
            buf += b"system_config_type=%s\x00" % (self._system_config_type)

        # parm_disk_owner (string,0-8,char42)
        if len(self._parm_disk_owner) > 0:
            buf += b"parm_disk_owner=%s\x00" % (self._parm_disk_owner)

        # parm_disk_number (string,0-4,char16)
        if len(self._parm_disk_number) > 0:
            buf += b"parm_disk_number=%s\x00" % (self._parm_disk_number)

        # parm_disk_password (string,0-8,charNB)
        if len(self._parm_disk_password) > 0:
            buf += b"parm_disk_password=%s\x00" % (self._parm_disk_password)

        return super(Page_or_Spool_Volume_Add, self).pack(buf)

