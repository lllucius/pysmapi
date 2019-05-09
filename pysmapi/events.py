
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

import copy
import struct
import threading

import pysmapi as smapi

# ==============================================================================
# 
# ==============================================================================
class Events(threading.Thread):
    type0_formats = {
        "0_0":  ["#8s"],
        "0_1":  ["#8s"],
        "0_2":  ["#8s", "B"],
        "0_3":  ["#8s", "H"],
        "0_4":  ["#8s"],
        "0_5":  ["#8s"],
        "0_6":  ["#8s"],
        "0_9":  ["#8s", "#8s"],
        "0_10": ["#8s", "#8s"],
        "0_11": ["#8s", "#8s"],
        "0_12": ["#8s", "#8s"],
        "0_13": ["#8s", "B"],
        "0_14": ["#8s", "B"],
        "0_15": ["#8s"],
        "0_26": ["#8s", "B"],
        "0_27": ["#8s"],
        "1_2":  ["#8s", "B"],
        "1_3":  ["#8s", "H"],
        "1_4":  ["#8s"],
        "1_6":  ["#8s"],
        "1_9":  ["#8s", "#8s"],
        "1_10": ["#8s", "#8s"],
        "2_7":  ["#8s", "B", "B"],
        "2_8":  ["#8s", "#8s", "B", "B"],
        "3_7":  ["#8s", "B", "B"],
        "3_8":  ["#8s", "#8s", "B", "B"],
        "4_16": ["#8s", "#8s", "H", "B", "B", "H", "B", "B"],
        "4_17": ["#8s", "#8s", "H", "B", "B", "H", "B", "B"],
        "4_18": ["#8s", "#8s", "H", "B", "B", "H", "B", "B"],
        "4_19": ["#8s", "#8s", "H", "B", "B", "H", "B", "B"],
        "4_20": ["#8s", "H", "B", "B"],
        "4_21": ["#8s", "H", "B", "B"],
        "4_22": ["#8s", "#8s", "#8s", "#8s", "6s", "#8s", "H", "B", "B"],
        "4_23": ["#8s", "#8s", "#8s", "#8s", "6s", "#8s", "H", "B", "B"],
        "4_24": ["#8s", "B", "B"],
        "4_25": ["#8s", "B", "B"],
    }

    def __init__(self, hostinfo, target, match=None):
        super().__init__()

        # Kill the thread if process terminates
        self.daemon = True

        self._hostinfo = copy.copy(hostinfo)
        self._hostinfo.timeout = None
        self._target = target
        self._match = match

        self._type0_handler = self.type0_event
        self._type1_handler = self.type1_event

    def set_type0_handler(self, handler):
        self._type0_handler = handler

    def set_type1_handler(self, handler):
        self._type1_handler = handler

    def stop(self):
        smapi.Event_Unsubscribe(target=self._target).request(self._hostinfo)

    def run(self):
        self._req = smapi.Event_Subscribe()
        self._req.target = self._target
        self._req.match_key = self._match
        self._req.request(self._hostinfo)
        if self._req.failed():
            raise Exception(self._req.error_string())

        try:
            while True:
                try:
                    event_type, event_data = self._req.getevent()
                except IOError as e:
                    break

                if event_type == 0:
                    res = self.handle_type0(event_data)
                elif event_type == 1:
                    res = self.handle_type1(event_data)
                else:
                    raise ValueError(f"Unrecognized event type: {event_type}")
        finally:
            self.stop()

    def handle_type0(self, event_data):
        ndx = 0
        length = len(event_data)

        while ndx < length:
            # Get the class and type
            event_class, event_type = struct.unpack("!HH", event_data[ndx:ndx + 4])
            ndx += 4

            key = f"{event_class}_{event_type}"
            if key not in self.type0_formats:
                raise ValueError(f"Unrecognized type 0 event received: {key}")

            fields = []
            for fmt in self.type0_formats[key]:
                # Remember if we have to decode the field
                dec = False
                if fmt[0] == "#":
                    dec = True
                    fmt = fmt[1:]

                size = struct.calcsize(fmt)
                field, = struct.unpack(f"!{fmt}", event_data[ndx:ndx + size])
                if dec:
                    field = field.decode("cp924").strip()
                fields.append(field)

                ndx += size

            self._type0_handler(event_class, event_type, fields)

    def handle_type1(self, event_data):
        # Get the common response values
        (event_type,
         request_id,
         return_code,
         reason_code) = struct.unpack("!IIII", event_data[:16])

        # Remove the common response values
        event_data = event_data[16:]

        if event_type == 2:
            event_request = smapi.System_Performance_Threshold_Enable()
        elif event_type == 500:
            #
            # This event can be triggered by:
            #   Image_Definition_Create_DM
            #   Image_Definition_Update_DM
            #   Image_Definition_Delete_DM
            #
            # Unfortunately, the event doesn't indicate which, but all 3
            # have the same output format, so we just use "Create".
            #
            # However, if the "function_name" variable is referenced it will
            # always show as "Image_Definition_Create_DM" and this is apparent
            # when using the error_string() function.
            #
            event_request = smapi.Image_Definition_Create_DM()
        elif event_type == 2008 or event_type == 2010:
            event_request = smapi.Process_ABEND_Dump()
        elif event_type == 2009:
            event_request = smapi.Delete_ABEND_Dump()
        else:
            raise ValueError(f"Unrecognized type 1 event received: {event_type}")

        event_request.request_id = request_id
        event_request.return_code = return_code
        event_request.reason_code = reason_code

        if len(event_data) > 0:
            event_request.unpack(event_data)

        self._type1_handler(event_type, event_request)

    def type0_event(self, event_class, event_type, event_fields):
        pass
      
    def type1_event(self, event_type, event_request):
        pass

