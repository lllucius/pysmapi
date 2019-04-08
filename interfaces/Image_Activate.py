
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

class Image_Activate(Request):
    def __init__(self,
                 **kwargs):
        super(Image_Activate, self).__init__(**kwargs)

        # Response values
        self._activated = 0
        self._not_activated = 0
        self._failing_array = []

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, value):
        self._activated = value

    @property
    def not_activated(self):
        return self._not_activated

    @not_activated.setter
    def not_activated(self, value):
        self._not_activated = value

    @property
    def failing_array(self):
        return self._failing_array

    @failing_array.setter
    def failing_array(self, value):
        self._failing_array = value

    def unpack(self, buf):
        offset = 0

        # activated (int4)
        # not_activated (int4)
        # failing_array_length (int4)
        self._activated, \
        self._not_activated, \
        alen = struct.unpack("!III", buf[offset:offset + 12])
        offset += 12

        self._failing_array = []
        while alen > 0:
            entry = Obj()
            self._failing_array.append(entry)

            # failing_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # image_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # image_name (string,1-8,char42)
            entry.image_name = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen

            # return_code (int4)
            entry.return_code, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # reason_code (int4)
            entry.reason_code, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

