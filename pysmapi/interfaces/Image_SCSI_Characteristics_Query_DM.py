
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

class Image_SCSI_Characteristics_Query_DM(Request):

    # SCP data type
    UNSPECIFIED = 0
    EBCDIC = 2
    HEX = 3
    scp_data_type_names = {UNSPECIFIED: "UNSPECIFIED", EBCDIC: "EBCDIC", HEX: "HEX"}

    def __init__(self,
                 **kwargs):
        super(Image_SCSI_Characteristics_Query_DM, self).__init__(**kwargs)

        # Response values
        self._boot_program = ""
        self._br_lba = ""
        self._lun = ""
        self._port_name = ""
        self._scp_data_type = self.UNSPECIFIED
        self._scp_data = b""                        # <-- must be byte array

    @property
    def boot_program(self):
        return self._boot_program

    @boot_program.setter
    def boot_program(self, value):
        self._boot_program = value

    @property
    def br_lba(self):
        return self._br_lba

    @br_lba.setter
    def br_lba(self, value):
        self._br_lba = value

    @property
    def lun(self):
        return self._lun

    @lun.setter
    def lun(self, value):
        self._lun = value

    @property
    def port_name(self):
        return self._port_name

    @port_name.setter
    def port_name(self, value):
        self._port_name = value

    @property
    def scp_data_type(self):
        return self._scp_data_type

    @scp_data_type.setter
    def scp_data_type(self, value):
        self._scp_data_type = value

    @property
    def scp_data(self):
        return self._scp_data

    @scp_data.setter
    def scp_data(self, value):
        self._scp_data = value

    def unpack(self, buf):
        offset = 0

        # boot_program_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # boot_program (string,0-6,char10)
        self._boot_program = b2s(buf[offset:offset + nlen])
        offset += nlen

        # br_lba_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # br_lba (string,0-6,char10)
        self._br_lba = b2s(buf[offset:offset + nlen])
        offset += nlen

        # lun_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # lun (string,0-6,char10)
        self._lun = b2s(buf[offset:offset + nlen])
        offset += nlen

        # port_name_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # port_name (string,0-6,char10)
        self._port_name = b2s(buf[offset:offset + nlen])
        offset += nlen

        # scp_data_type (int1)
        self._scp_data_type = buf[offset]
        offset += 1

        # scp_data_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # scp_data (string,0-6,char10)
        self._scp_data = buf[offset:offset + nlen]      # <-- must be byte array
        offset += nlen

