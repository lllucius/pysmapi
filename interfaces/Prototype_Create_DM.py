
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

class Prototype_Create_DM(Request):
    def __init__(self,
                 prototype_record_array = [],
                 **kwargs):
        super(Prototype_Create_DM, self).__init__(**kwargs)

        # Request parameters
        self._prototype_record_array = prototype_record_array

    @property
    def prototype_record_array(self):
        return self._prototype_name

    @prototype_record_array.setter
    def prototype_record_array(self, value):
        self._prototype_record_array = value

    def pack(self):
        alen = 0
        buf = ""
        for prototype_record in self._prototype_record_array:
            ir_len = len(prototype_record)

            # prototype_record_length (int4)
            # prototype_record (string,1-72,charNA)
            fmt = "!I%ds" % (ir_len)
            buf += struct.pack(fmt,
                               ir_len,
                               bytes(prototype_record, "UTF-8"))
            alen += ir_len + 4

        # prototype_record_array_length (int4)
        # prototype_record_array
        buf = struct.pack(alen) + buf

        return buf
