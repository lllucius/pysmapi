
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

class Event_Unsubscribe(Request):
    def __init__(self,
                 **kwargs):
        super(Event_Unsubscribe, self).__init__(**kwargs)

    def request(self, hostinfo, wait=True, interval=INTERVAL):
        # Save host info
        self._hinfo = hostinfo

        # Must connect to the SMAPI host for each request
        self.connect()

        # Send the request
        self.send(b"")

        # At this point SMAPI has only accepted the request and hasn't yet
        # acted upon it

        # Get the immediate request ID
        self._request_id, = struct.unpack("!I", self.recv(4))

