
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

class Virtual_Network_OSA_Query(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(Virtual_Network_OSA_Query, self). \
            __init__(b"Virtual_Network_OSA_Query", **kwargs)

        # Response values
        self._osa_info_array = []

    @property
    def osa_info_array(self):
        return self._osa_info_array

    @osa_info_array.setter
    def osa_info_array(self, value):
        self._osa_info_array = value

    def unpack(self, buf, offset):
        offset = super(Virtual_Network_OSA_Query, self).unpack(buf, offset)

        buf = buf[offset:]

        self._osa_info_array = buf[:-1].split(b"\x00")

        offset += len(buf)

        return offset

