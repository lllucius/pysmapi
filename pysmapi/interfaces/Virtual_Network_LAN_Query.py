
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

class Virtual_Network_LAN_Query(Request):
    # LAN type
    HIPERSOCKET = 1
    QDIO = 2
    lan_type_names = {HIPERSOCKET: "HIPERSOCKET", QDIO: "QDIO"}

    def __init__(self,
                 lan_name = "",
                 lan_owner = "",
                 **kwargs):
        super(Virtual_Network_LAN_Query, self).__init__(**kwargs)

        # Request parameters
        self._lan_name = lan_name
        self._lan_owner = lan_owner

        # Response values
        self._lan_info_array = []

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
    def lan_info_array(self):
        return self._lan_info_array

    @lan_info_array.setter
    def lan_info_array(self, value):
        self._lan_info_array = value

    def pack(self):
        ln_len = len(self._lan_name)
        lo_len = len(self._lan_owner)

        # lan_name_length (int4)
        # lan_name (string,1-8,char36 plus $#@)
        # lan_owner_length (int4)
        # lan_owner (string,1-8,char42)
        #           (string,6,SYSTEM)
        fmt = "!I%dsI%ds" % (ln_len, lo_len)

        buf = struct.pack(fmt,
                          ln_len,
                          s2b(self._lan_name),
                          lo_len,
                          s2b(self._lan_owner))

        return buf

    def unpack(self, buf):
        offset = 0

        # lan_info_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._lan_info_array = []
        while alen > 0:
            entry = Obj()
            self._lan_info_array.append(entry)

            # lan_info_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # lan_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # lan_name (string,1-8,char36 plus $#@)
            entry.lan_name = b2s(buf[offset:offset + nlen])
            offset += nlen

            # lan_owner_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # lan_owner (string,1-8,char42)
            entry.lan_owner = b2s(buf[offset:offset + nlen])
            offset += nlen

            # lan_type (int1)
            entry.lan_type = buf[offset]
            offset += 1

            # connected_adapter_array_length (int4)
            clen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (clen + 4)

            entry.connected_adapter_array = []
            while clen > 0:
                adapter = Obj()
                entry.connected_adapter_array.append(adapter)

                # connected_adapter_structure_length (int4)
                slen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4
                clen -= (slen + 4)

                # adapter_owner_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # adapter_owner (string,1-8,char42)
                adapter.adapter_owner = b2s(buf[offset:offset + nlen])
                offset += nlen

                # image_device_number_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # image_device_number (string,1-4,char16)
                adapter.image_device_number = b2s(buf[offset:offset + nlen])
                offset += nlen

