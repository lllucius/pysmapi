
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

class System_Performance_Threshold_Enable(Smapi_Request_Base):
    def __init__(self,
                 event_type = b"",
                 **kwargs):
        super(System_Performance_Threshold_Enable, self). \
            __init__(b"System_Performance_Threshold_Enable", **kwargs)

        # Request parameters
        self._event_type = event_type

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    def pack(self):
        # event_type (string,1-26,char42 plus blank plus /)
        buf = b"%s\x00" % (self._event_type)
        
        return super(System_Performance_Threshold_Enable, self).pack(buf)

