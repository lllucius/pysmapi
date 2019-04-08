
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

class Virtual_Network_LAN_Access(Request):
    def __init__(self,
                 lan_name = "",
                 lan_owner = "",
                 access_op = "",
                 access_user = "",
                 promiscuity = "",
                 **kwargs):
        super(Virtual_Network_LAN_Access, self).__init__(**kwargs)

        # Request parameters
        self._lan_name = lan_name
        self._lan_owner = lan_owner
        self._access_op = access_op
        self._access_user = access_user
        self._promiscuity = promiscuity

    @property
    def lan_name(self):
        return self._lan_name

    @lan_name.setter
    def lan_name(self, value):
        self._lan_name = value

    @property
    def lan_owner(self):
        return self._lan_owner

    @lan_owner.setter
    def lan_owner(self, value):
        self._lan_owner = value

    @property
    def access_op(self):
        return self._access_op

    @access_op.setter
    def access_op(self, value):
        self._access_op = value

    @property
    def access_user(self):
        return self._access_user

    @access_user.setter
    def access_user(self, value):
        self._access_user = value

    @property
    def promiscuity(self):
        return self._promiscuity

    @promiscuity.setter
    def promiscuity(self, value):
        self._promiscuity = value

    def pack(self):
        buf = ""

        # lan_name (string,1-8,char36 plus $#@)
        buf += f"{self._lan_name}\x00"

        # lan_owner (string,1-8,char36)
        buf += f"self._lan_owner\x00"

        # access_op (string,5,GRANT)
        #           (string,6,REVOKE)
        buf += f"{self._access_op}\x00"

        # access_user (string,1-8,char36)
        buf += f"{self._access_user}\x00"

        # promiscuity (string,14,NONPROMISCUOUS)
        #             (string,11,PROMISCUOUS)
        buf += f"{self._promiscuity}\x00"

        return bytes(buf, "UTF-8")
