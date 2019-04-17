
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

class Image_Lock_Query_DM(Request):
    def __init__(self,
                 **kwargs):
        super(Image_Lock_Query_DM, self).__init__(**kwargs)

        # Response values
        self._locked_type = ""
        self._image_locked_by = ""
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

    def unpack(self, buf):
        offset = 0

        # lock_info_structure_length (int4)
        slen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # locked_type (string,5-6,char26)
        # image_locked_by (string,0-8,char42)
        # locked_dev_array_length (int4)
        self._locked_type, \
        _, \
        self._image_locked_by = b2s(buf[offset:offset + slen]).partition(" ")
        offset += slen

        # locked_dev_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        if alen:
            # locked_dev_array
            self._locked_dev_array = []
            for info in b2s(buf[offset:offset + alen - 1]).split("\x00"):
                entry = Obj()
                self._locked_dev_array.append(entry)

                # dev_address (string,1-4,char16)
                # dev_locked_by (string,1-8,char42)
                entry.dev_address, \
                entry.dev_locked_by = info.split()

