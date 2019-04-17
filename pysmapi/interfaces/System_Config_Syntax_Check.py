
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

class System_Config_Syntax_Check(Request):
    def __init__(self,
                 system_config_name = "",
                 system_config_type = "",
                 parm_disk_owner = "",
                 parm_disk_number = "",
                 parm_disk_password = "",
                 **kwargs):
        super(System_Config_Syntax_Check, self).__init__(**kwargs)

        # Request parameters
        self._system_config_name = system_config_name
        self._system_config_type = system_config_type
        self._parm_disk_owner = parm_disk_owner
        self._parm_disk_number = parm_disk_number
        self._parm_disk_password = parm_disk_password

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
        buf = ""

        # system_config_name (string,0-8,char42)
        if len(self._system_config_name) > 0:
            buf += "system_config_name=%s\x00" % (self._system_config_name)

        # system_config_type (string,0-8,char42)
        if len(self._system_config_type) > 0:
            buf += "system_config_type=%s\x00" % (self._system_config_type)

        # parm_disk_owner (string,0-8,char42)
        if len(self._parm_disk_owner) > 0:
            buf += "parm_disk_owner=%s\x00" % (self._parm_disk_owner)

        # parm_disk_number (string,0-4,char16)
        if len(self._parm_disk_number) > 0:
            buf += "parm_disk_number=%s\x00" % (self._parm_disk_number)

        # parm_disk_password (string,0-8,charNB)
        if len(self._parm_disk_password) > 0:
            buf += "parm_disk_password=%s\x00" % (self._parm_disk_password)

        return s2b(buf)
