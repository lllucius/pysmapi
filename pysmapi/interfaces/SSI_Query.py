
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

class SSI_Query(Request):

    def __init__(self,
                 **kwargs):
        super(SSI_Query, self).__init__(**kwargs)

        # Response values
        self._ssi_name = ""
        self._ssi_mode = ""
        self._cross_system_timeouts = ""
        self._ssi_pdr = ""
        self._ssi_info_array = []

    @property
    def ssi_name(self):
        return self._ssi_name

    @ssi_name.setter
    def ssi_name(self, value):
        self._ssi_name = value

    @property
    def ssi_mode(self):
        return self._ssi_mode

    @ssi_mode.setter
    def ssi_mode(self, value):
        self._ssi_mode = value

    @property
    def cross_system_timeouts(self):
        return self._cross_system_timeouts

    @cross_system_timeouts.setter
    def cross_system_timeouts(self, value):
        self._cross_system_timeouts = value

    @property
    def ssi_pdr(self):
        return self._ssi_pdr

    @ssi_pdr.setter
    def ssi_pdr(self, value):
        self._ssi_pdr = value

    @property
    def ssi_info_array(self):
        return self._ssi_info_array

    @ssi_info_array.setter
    def ssi_info_array(self, value):
        self._ssi_info_array = value

    def unpack(self, buf):
        offset = 0

        buf = b2s(buf[offset:-1]).split("\x00")
        offset += len(buf)

        # ssi_name (string,1-8,char42)
        self._ssi_name = buf[0]

        # ssi_mode (string,4-6,char26)
        self._ssi_mode = buf[1]

        # cross_system_timeouts (string,7-8,char26)
        self._cross_system_timeouts = buf[2]

        # ssi_pdr (string,6-14,char42)
        self._ssi_pdr = buf[3]

        # ssi_info_array
        self._ssi_info_array = []
        for info in buf[4:]:
            entry = Obj()
            self._ssi_info_array.append(entry)

            info = info.split(" ")

            # member_slot (string,1,char10)
            entry.member_slot = info[0]

            # member_system_id (string,1-8,char42)
            entry.member_system_id = info[1]

            # member_state (string,4-9,char26)
            entry.member_state = info[2]

            # member_pdr_heartbeat (string,19,char43 plus /)
            entry.member_pdr_heartbeat = info[3]

            # member_received_heartbeat (string,19,char43 plus /)
            entry.member_received_heartbeat = info[4]

