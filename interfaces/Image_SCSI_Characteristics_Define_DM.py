
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

class Image_SCSI_Characteristics_Define_DM(Request):

    # SCP data type
    UNSPECIFIED = 0
    DELETE = 1
    EBCDIC = 2
    HEX = 3
    scp_data_type_names = ["UNSPECIFIED", "DELETE", "EBCDIC", "HEX"]

    def __init__(self,
                 boot_program = "",
                 br_lba = "",
                 lun = "",
                 port_name = "",
                 scp_data_type = 0,
                 scp_data = b"",            # <-- must be byte array
                 **kwargs):
        super(Image_SCSI_Characteristics_Define_DM, self).__init__(**kwargs)

        # Request parameters
        self._boot_program = boot_program
        self._br_lba = br_lba
        self._lun = lun
        self._port_name = port_name
        self._scp_data_type = scp_data_type
        self._scp_data = scp_data

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

    def pack(self):
        bp_len = len(self._boot_program)
        bl_len = len(self._br_lba)
        l_len = len(self._lun)
        pn_len = len(self._port_name)
        sd_len = len(self._scp_data)

        # boot_program_length (int4)
        # boot_program (string,0-6,char10
        # br_lba_length (int4)
        # BR_LBA (string,0-16,char16)
        # lun_length (int4)
        # LUN (string,0-16,char16)
        # port_name (int4)
        # port_name (string,0-16,char16)
        # scp_data_type (int1)
        # scp_data_length (int4)
        # scp_data (string,0-4096,charNA)
        fmt = "!I%dsI%dsI%dsI%dsBI%ds" % \
            (bp_len,
             bl_len,
             l_len,
             pn_len,
             sd_len)

        buf = struct.pack(fmt,
                          bp_len,
                          bytes(self._boot_program, "UTF-8"),
                          bl_len,
                          bytes(self._br_lba, "UTF-8"),
                          l_len,
                          bytes(self._lun, "UTF-8"),
                          pn_len,
                          bytes(self._port_name, "UTF-8"),
                          self._scp_data_type,
                          sd_len,
                          self._scp_data) # <--- must be byte array

        return buf
