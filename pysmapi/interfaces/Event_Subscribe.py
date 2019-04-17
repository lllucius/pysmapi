
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

from pysmapi.smapi import *

class Event_Subscribe(Request):
    def __init__(self,
                 match_key = "",
                 **kwargs):
        super(Event_Subscribe, self).__init__(**kwargs)

        # Request values
        self._match_key = match_key

        # Response values
        self._response_data = ""

    def __del__(self):
        if getattr(self, "_socket", None):
            self.disconnect()

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

    # Returns the next available event
    def getevent(self):
        # We may receive the common response values or we may receive an empty
        # response.  The former means the subscription failed, while the latter
        # means it was succesful and we leave the socket open for receiving more
        # data.
        length, = struct.unpack("!I", self.recv(4))

        # Get the failure information (common response values)
        if length == 12:
            (self._request_id,
             self._return_code,
             self._reason_code) = struct.unpack("!III", self.recv(12))

            if smapi.debugging:
                print(self.request_id)
                print(self.return_code)
                print(self.reason_code)

            self.disconnect()

            return

        # Get the event length
        event_type = struct.unpack("!I", self.recv(4))
        length -= 4

        # Get the event data
        event_data = self.recv(length) if length > 0 else ""

        return event_type, event_data

    @property
    def match_key(self):
        return self._match_key

    @match_key.setter
    def match_key(self, value):
        self._match_key = value

    def pack(self):
        mk_len = len(self._match_key)

        fmt = "!I%ds" % (mk_len)

        # match_key (int4)
        # match_key (string,0-16M,charNA)
        buf = struct.pack(fmt,
                          mk_len,
                          s2b(self._match_key))

        return buf
