
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

class Image_Deactivate(Smapi_Request_Base):
    def __init__(self,
                 force_time = b"",
                 **kwargs):
        super(Image_Deactivate, self). \
            __init__(b"Image_Deactivate", **kwargs)

        # Request parameters
        self._force_time = force_time

        # Response values
        self._deactivated = 0
        self._not_deactivated = 0
        self._failing_array = []

    @property
    def force_time(self):
        return self._force_time

    @force_time.setter
    def force_time(self, value):
        self._force_time = value

    @property
    def deactivated(self):
        return self._deactivated

    @deactivated.setter
    def deactivated(self, value):
        self._deactivated = value

    @property
    def not_deactivated(self):
        return self._not_deactivated

    @not_deactivated.setter
    def not_deactivated(self, value):
        self._not_deactivated = value

    @property
    def failing_array(self):
        return self._failing_array

    @failing_array.setter
    def failing_array(self, value):
        self._failing_array = value

    def pack(self):
        ft_len = len(self._force_time)

        # force_time_length (int4)
        # force_time (string,0-12,char42)
        fmt = b"!I%ds" % (ft_len)
        buf = struct.pack(fmt,
                          ft_len,
                          self._force_time)

        return super(Image_Create_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Image_Deactivate, self).unpack(buf, offset)

        # deactivated (int4)
        # not_deactivated (int4)
        # failing_array_length (int4)
        self._deactivated, \
        self._not_deactivated, \
        alen = struct.unpack(b"!III", buf[offset:offset + 12])
        offset += 12

        self._failing_array = []
        while alen > 0:
            entry = Obj()
            self._failing_array.append(entry)

            # failing_structure_length (int4)
            slen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # image_name_length (int4)
            nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # image_name (string,1-8,char42)
            entry.image_name = buf[offset:offset + nlen]
            offset += nlen

            # return_code (int4)
            entry.return_code, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # reason_code (int4)
            entry.reason_code, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

        return offset

