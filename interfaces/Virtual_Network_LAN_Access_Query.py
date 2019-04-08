
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

class Virtual_Network_LAN_Access_Query(Request):
    def __init__(self,
                 lan_name = "",
                 lan_owner = "",
                 **kwargs):
        super(Virtual_Network_LAN_Access_Query, self).__init__(**kwargs)

        # Request parameters
        self._lan_name = lan_name
        self._lan_owner = lan_owner

        # Response values
        self._authorized_users_array = []

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
    def authorized_users_array(self):
        return self._authorized_users_array

    @authorized_users_array.setter
    def authorized_users_array(self, value):
        self._authorized_users_array = value

    def pack(self):
        buf = ""

        # lan_name (string,1-8,char36 plus $#@)
        buf += f"{self._lan_name}\x00"

        # lan_owner (string,1-8,char36)
        buf += f"{self._lan_owner}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):

        self._authorized_users_array = []

        # authorized_user_record (string,1-23,char36)
        for record in buf[:-1].decode("UTF-8").split("\x00"):
            entry = Obj()
            self._authorized_users_array.append(entry)

            entry.name,
            entry.promiscuity = record.split()

