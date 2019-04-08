
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

class Virtual_Network_OSA_Query(Request):
    def __init__(self,
                 **kwargs):
        super(Virtual_Network_OSA_Query, self).__init__(**kwargs)

        # Response values
        self._osa_info_array = []

    @property
    def osa_info_array(self):
        return self._osa_info_array

    @osa_info_array.setter
    def osa_info_array(self, value):
        self._osa_info_array = value

    def unpack(self, buf):
        for info in buf[:-1].decode("UTF-8").split("\x00"):
            entry = Obj()
            self._osa_info_array.append(entry)

            fields = info.split()

            # osa_address (string,4,char16)
            entry.osa_address = fields[0]

            # osa_status(string,4-16,char42)
            entry.osa_status = fields[1]

            # osa_type (string,3-7,char26)
            entry.osa_type = fields[2]

            # chpid_address (string,2,char16)
            entry.chpid_address = fields[3]

            # agent_status (string,2-3,char42)
            entry.agent_status = fields[4]

