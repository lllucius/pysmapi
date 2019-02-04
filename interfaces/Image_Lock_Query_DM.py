
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

class Image_Lock_Query_DM(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(Image_Lock_Query_DM, self). \
            __init__(b"Image_Lock_Query_DM", **kwargs)

        # Response values
        self._locked_type = b""
        self._image_locked_by = b""
        self._locked_dev_array = []

    @property
    def locked_type(self):
        return self._locked_type

    @locked_type.setter
    def locked_type(self, value):
        self._locked_type = value

    @property
    def image_locked_by(self):
        return self._image_locked_by

    @image_locked_by.setter
    def image_locked_by(self, value):
        self._image_locked_by = value

    @property
    def locked_dev_array(self):
        return self._locked_dev_array

    @locked_dev_array.setter
    def locked_dev_array(self, value):
        self._locked_dev_array = value

    def unpack(self, buf, offset):
        offset = super(Image_Lock_Query_DM, self).unpack(buf, offset)

        # lock_info_structure_length (int4)
        slen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # locked_type (string,5-6,char26)
        # image_locked_by (string,0-8,char42)
        # locked_dev_array_length (int4)
        if slen > 0:
            self._locked_type, _, self._image_locked_by = \
                buf[offset:offset + slen].partition(" ")
            offset += slen

        # locked_dev_array_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # locked_dev_array
        self._locked_dev_array = []
        while alen > 0:
            entry = Obj()
            self._locked_dev_array.append(entry)

            # dev_address (string,1-4,char16)
            # dev_locked_by (string,1-8,char42)
            entry.dev_address,
            entry.dev_locked_by = struct.unpack(b"4s8s", buf[offset:offset + 12])
            offset += 12
            alen -= 12

        return offset

