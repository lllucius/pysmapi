
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

class Query_Asynchronous_Operation_DM(Request):
    def __init__(self,
                 operation_id = "",
                 **kwargs):
        super(Query_Asynchronous_Operation_DM, self).__init__(**kwargs)

        # Request parameters
        self._operation_id = operation_id

    @property
    def operation_id(self):
        return self._operation_id

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = value

    def pack(self, **kwargs):
        # operation_id (int4; range 0-2147483647)
        buf = struct.pack(self._operation_id)
 
        return buf
