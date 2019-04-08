
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

class Event_Stream_Add(Request):
    def __init__(self,
                 event_info = "",
                 **kwargs):
        super(Event_Stream_Add, self).__init__(**kwargs)

        # Request parameters
        self._event_info = event_info

    @property
    def event_info(self):
        return self._event_info

    @event_info.setter
    def event_info(self, value):
        self._event_info = value

    def pack(self, **kwargs):
        # event_info (string,1-maxlength,charNA)
        buf = bytes(self._event_info, "UTF-8")

        return buf
