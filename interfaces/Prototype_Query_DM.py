
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

class Prototype_Query_DM(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(Prototype_Query_DM, self). \
            __init__(b"Prototype_Query_DM", **kwargs)

        # Response values
        self._prototype_record_array = []

    @property
    def prototype_record_array(self):
        return self._prototype_record_array

    @prototype_record_array.setter
    def prototype_record_array(self, value):
        self._prototype_record_array = value

    def unpack(self, buf, offset):
        offset = super(Prototype_Query_DM, self).unpack(buf, offset)

        # prototype_record_array_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # prototype_record_array
        self._prototype_record_array = []
        while alen > 0:
            # prototype_record_length (int4)
            nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # prototype_record (string,1-80,charNA)
            self._prototype_record_array.append(buf[offset:offset + nlen])
            offset += nlen

            alen -= (nlen + 4)

        return offset

