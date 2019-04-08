
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

class Virtual_Network_Vswitch_Delete(Request):
    # Update system config indicator
    UNSPECIFIED = 0
    ACTIVEONLYL = 1
    BOTH = 2
    CONFIGONLY = 3

    def __init__(self,
                 switch_name = "",
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
                 **kwargs):
        super(Virtual_Network_Vswitch_Delete, self).__init__(**kwargs)

        # Request parameters
        self._switch_name = switch_name
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

    @property
    def switch_name(self):
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value):
        self._switch_name = value

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

    def pack(self):
        sn_len = len(self._switch_name)
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
        fmt = "!I%dsBI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%ds" % \
            (sn_len,
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
                          bytes(self._switch_name, "UTF-8"),
                          self._update_system_config_indicator,
                          scn_len,
                          bytes(self._system_config_name, "UTF-8"),
                          sct_len,
                          bytes(self._system_config_type, "UTF-8"),
                          pdo_len,
                          bytes(self._parm_disk_owner, "UTF-8"),
                          pdn_len,
                          bytes(self._parm_disk_number, "UTF-8"),
                          pdp_len,
                          bytes(self._parm_disk_password, "UTF-8"),
                          ascn_len,
                          bytes(self._alt_system_config_name, "UTF-8"),
                          asct_len,
                          bytes(self._alt_system_config_type, "UTF-8"),
                          apdo_len,
                          bytes(self._alt_parm_disk_owner, "UTF-8"),
                          apdn_len,
                          bytes(self._alt_parm_disk_number, "UTF-8"),
                          apdp_len,
                          bytes(self._alt_parm_disk_password, "UTF-8"))

        return buf

