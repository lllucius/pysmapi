
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

class Event_Unsubscribe(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(Event_Unsubscribe, self). \
            __init__(b"Event_Unsubscribe", **kwargs)

    def request(self, conn, wait=True):
        conn.connect()

        conn.send(self.pack())

        # At this point SMAPI has only accepted the request and hasn't yet
        # acted upon it

        # Get the immediate request ID
        self._request_id, = struct.unpack("!I", conn.recv(4))

        conn.disconnect()

