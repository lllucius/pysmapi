
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

class Directory_Manager_Task_Cancel_DM(Smapi_Request_Base):
    def __init__(self,
                 operation_id = b"",
                 **kwargs):
        super(Directory_Manager_Task_Cancel_DM, self). \
            __init__(b"Directory_Manager_Task_Cancel_DM", **kwargs)

        # Request parameters
        self._operation_id = operation_id

    @property
    def operation_id(self):
        return self._operation_id

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = value

    def pack(self):
        # operation_id (int4; range 0-2147483647)
        buf = struct.pack(b"!I", self._operation_id)

        return super(Directory_Manager_Task_Cancel_DM, self).pack(buf)

