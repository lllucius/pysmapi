
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

from base import Smapi_Request_Base, Obj

class Image_Active_Configuration_Query(Smapi_Request_Base):

    # Memory unit
    KB = 1
    MB = 2
    GB = 3
    memory_unit_names = ["?", "KB", "MB", "GB"]

    # Share type
    RELATIVE = 1
    ABSOLUTE = 2
    share_type_names = ["?", "RELATIVE", "ABSOLUTE"]

    # CPU Status
    BASE = 1
    STOPPED = 2
    CHECK_STOPPED = 3
    NON_BASE_ACTIVE = 4
    cpu_state_names = ["?", "BASE", "STOPPED", "CHECK STOPPED", "NON-BASE, ACTIVE"]

    # Device type
    CONS = 1
    RDR = 2
    PUN = 3
    PRT = 4
    DASD = 5
    device_type_names = ["?", "CONS", "RDR", "PUN", "PRT", "DASD"]

    def __init__(self,
                 **kwargs):
        super(Image_Active_Configuration_Query, self). \
            __init__(b"Image_Active_Configuration_Query", **kwargs)

        # Response values
        self._memory_size = 0
        self._memory_unit = 0
        self._share_type = 0
        self._share_value = b""
        self._number_cpus = 0
        self._cpu_info_array = []
        self._device_info_array = []

    @property
    def memory_size(self):
        return self._memory_size

    @memory_size.setter
    def memory_size(self, value):
        self._memory_size = value

    @property
    def memory_unit(self):
        return self._memory_unit

    @memory_unit.setter
    def memory_unit(self, value):
        self._memory_unit = value

    @property
    def share_type(self):
        return self._share_type

    @share_type.setter
    def share_type(self, value):
        self._share_type = value

    @property
    def share_value(self):
        return self._share_value

    @share_value.setter
    def share_value(self, value):
        self._share_value = value

    @property
    def number_cpus(self):
        return self._number_cpus

    @number_cpus.setter
    def number_cpus(self, value):
        self._number_cpus = value

    @property
    def cpu_info_array(self):
        return self._cpu_info_array

    @cpu_info_array.setter
    def cpu_info_array(self, value):
        self._cpu_info_array = value

    @property
    def device_info_array(self):
        return self._device_info_array

    @device_info_array.setter
    def device_info_array(self, value):
        self._device_info_array = value

    def unpack(self, buf, offset):
        offset = super(Image_Active_Configuration_Query, self).unpack(buf, offset)

        # memory_size (int4)
        # memory_unit (int1)
        # share_type (int1)
        # share_value_length (int4)
        self._memory_size, \
        self._memory_unit, \
        self._share_type, \
        alen = struct.unpack(b"!IBBI", buf[offset:offset + 10])
        offset += 10

        # share_value(string,1-5,char10 plus .)
        self._share_value = buf[offset:offset + alen]
        offset += alen

        # number_CPUs (int4)
        # CPU_info_array_length (int4)
        self._number_cpus, \
        alen = struct.unpack("!II", buf[offset:offset + 8])
        offset += 8

        self._cpu_info_array = []
        while alen > 0:
            entry = Obj()
            self._cpu_info_array.append(entry)

            # CPU_info_structure_length (int4)
            slen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # CPU_number (int4)
            # CPU_id_length (int4)
            entry.cpu_number, \
            nlen = struct.unpack(b"!II", buf[offset:offset + 8])
            offset += 8

            # CPU_id (string,1-16,char16)
            entry.cpu_id = buf[offset:offset + nlen]
            offset += nlen

            # CPU_status (int1)
            entry.cpu_status = ord(buf[offset])
            offset += 1

        # device_info_array_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        self._device_info_array = []
        while alen > 0:
            entry = Obj()
            self._device_info_array.append(entry)

            # device_info_structure_length (int4)
            slen, = struct.unpack(b"!I", buf[offset:offset + 4]) 
            offset += 4
            alen -= (slen + 4)

            # device_type (int1)
            entry.device_type = ord(buf[offset])
            offset += 1

            # device_address_length (int4)
            nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # device_address (string,4,char16)
            entry.device_address = buf[offset:offset + nlen]
            offset += nlen

        return offset

