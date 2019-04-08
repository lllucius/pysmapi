
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

class System_EQID_Query(Request):
    def __init__(self,
                 eqid_for = "",
                 eqid_target = "",
                 **kwargs):
        super(System_EQID_Query, self).__init__(**kwargs)

        # Request parameters
        self._eqid_for = eqid_for
        self._eqid_target = eqid_target

        # Response values
        self._eqid_array = []
        self._error_data = ""

    @property
    def eqid_for(self):
        return self._eqid_for

    @eqid_for.setter
    def eqid_for(self, value):
        self._eqid_for = value

    @property
    def eqid_target(self):
        return self._eqid_target

    @eqid_target.setter
    def eqid_target(self, value):
        self._eqid_target = value

    @property
    def eqid_array(self):
        return self._eqid_array

    @eqid_array.setter
    def eqid_array(self, value):
        self._eqid_array = value

    @property
    def error_data(self):
        return self._error_data

    @error_data.setter
    def error_data(self, value):
        self._error_data = value

    def pack(self):
        # eqid_for=value (string,3-4,char26)
        buf = f"eqid_for={self._eqid_for}\x00"

        # eqid_target=eqid_name (string,1-maxlength,char36)
        #             eqid_rdev (string,1-maxlength,char37)
        buf += f"eqid_target={self._eqid_target}\x00"

        return bytes(buf, "UTF-8")

    def unpack(self, buf):
        offset = 0

        # eqid_array_length (int4)
        #   or
        # error_data_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        if self.return_code == 0 and self.reason_code == 0:
            # eqid_array
            for eqid in buf[offset:-1].decode("UTF-8").split("\x00"):
                entry = Obj()
                self._eqid_array.append(entry)

                if self._eqid_for.upper() == "EQID":
                    # eqid_name (string,1-50,char26)
                    # eqid_rdev (string,1-maxlength,char16)
                    entry.eqid_name, \
                    _, \
                    entry.eqid_rdev = eqid.partition(" ")
                elif self._eqid_for.upper() in ["RDEV"]:
                    # eqid_rdev (string,1-4,char16 plus -)
                    # eqid_name (string,1-50,char36)
                    entry.eqid_rdev, \
                    entry.eqid_name = eqid.split(" ")
        elif self.return_code == 8 and self.reason_code in [3002, 3003]:
            # error_data (string)
            self._error_data, = buf[offset:-1].decode("UTF-8").split("\x00")

        offset += alen

