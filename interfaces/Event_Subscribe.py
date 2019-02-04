
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
import copy

from base import Smapi_Request_Base, Obj

class Event_Subscribe(Smapi_Request_Base):
    def __init__(self,
                 match_key = b"",
                 **kwargs):
        super(Event_Subscribe, self). \
            __init__(b"Event_Subscribe", **kwargs)

        # Request values
        self._match_key = match_key

        # Response values
        self._response_data = b""

        # Private copy of connection object
        self._conn = None

    def __del__(self):
        if self._conn is not None:
            self._conn.disconnect()
        self._conn = None

    def request(self, conn, wait=True):
        # Copy the connection object so the caller may continue to use it
        # for further requests (like unsubscribing)
        self._conn = copy.copy(conn)

        self._conn.connect()

        self._conn.send(self.pack())

        # At this point SMAPI has only accepted the request and hasn't yet
        # acted upon it

        # Get the immediate request ID
        self._request_id, = struct.unpack("!I", self._conn.recv(4))

    # Returns the next available event
    def getevent(self):
        # We may receive the common response values or we may receive an empty
        # response.  The former means the subscription failed, while the latter
        # means it was succesful and we leave the socket open for receiving more
        # data.
        length, = struct.unpack("!I", self._conn.recv(4))

        # Get the failure information (common response values)
        if length == 12:
            (self._request_id,
             self._return_code,
             self._reason_code) = struct.unpack("!III", self._conn.recv(12))

            print("REQUEST_ID", self.request_id)
            print("RETURN_CODE", self.return_code)
            print("REASON_CODE", self.reason_code)

            self._conn.disconnect()

            return

        # Get the event length
        event_type = struct.unpack("!I", self._conn.recv(4))
        length -= 4

        # Get the event data
        event_data = self._conn.recv(length) if length > 0 else b""

        return event_type, event_data

    @property
    def match_key(self):
        return self._match_key

    @match_key.setter
    def match_key(self, value):
        self._match_key = value

    def pack(self):
        mk_len = len(self._match_key)

        fmt = b"!I%ds" % (mk_len)

        # match_key (int4)
        # match_key (string,0-16M,charNA)
        buf = struct.pack(fmt,
                          mk_len,
                          self._match_key)

        return super(Event_Subscribe, self).pack(buf)

