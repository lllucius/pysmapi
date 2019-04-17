
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

class Image_CPU_Query_DM(Request):
    # (shared)
    UNSPECIFIED = 0

    # Base cpu
    BASE = 1
    base_cpu_names = {UNSPECIFIED: "UNSPECIFIED", BASE: "BASE"}

    # Dedicate cpu
    NODEDICATE = 1
    DEDICATE = 2
    dedicate_cpu_names = {NODEDICATE: "NODEDICATE", DEDICATE: "DEDICATE"}

    # Crypto
    CRYPTO = 1
    crypto_names = {UNSPECIFIED: "UNSPECIFIED", CRYPTO: "CRYPTO"}

    def __init__(self,
                 cpu_address = "",
                 **kwargs):
        super(Image_CPU_Query_DM, self).__init__(**kwargs)

        # Request parameters
        self._cpu_address = cpu_address

        # Response values
        self._base_cpu = 0
        self._cpuid = ""
        self._dedicate_cpu = 0
        self._crypto = 0

    @property
    def cpu_address(self):
        return self._cpu_address

    @cpu_address.setter
    def cpu_address(self, value):
        self._cpu_address = value

    @property
    def base_cpu(self):
        return self._cpu_address

    @base_cpu.setter
    def base_cpu(self, value):
        self._base_cpu = value

    @property
    def cpuid(self):
        return self._cpu_address

    @cpuid.setter
    def cpuid(self, value):
        self._cpuid = value

    @property
    def dedicate_cpu(self):
        return self._cpu_address

    @dedicate_cpu.setter
    def dedicate_cpu(self, value):
        self._dedicate_cpu = value

    @property
    def crypto(self):
        return self._cpu_address

    @crypto.setter
    def crypto(self, value):
        self._crypto = value

    def pack(self):
        ca_len = len(self._cpu_address)

        # cpu_address_length (int4)
        # cpu_address (string,1-2,char16)
        fmt = "!I%ds" % (ca_len)
        buf = struct.pack(fmt,
                          ca_len,
                          s2b(self._cpu_address))

        return buf

    def unpack(self, buf):
        offset = 0

        # cpu_address_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # cpu_address (string,2,char16)
        self._cpu_address = b2s(buf[offset:offset + nlen])
        offset += nlen

        # base_cpu (int1)
        self._base_cpu = buf[offset]
        offset += 1

        # cpuid_length (int4)
        nlen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # cpuid (string,6,char16)
        self._cpuid = b2s(buf[offset:offset + nlen])
        offset += nlen

        # dedicate_cpu (int1)
        self._dedicate_cpu = buf[offset]
        offset += 1

        # crypto (int1)
        self._crypto = buf[offset]
        offset += 1

