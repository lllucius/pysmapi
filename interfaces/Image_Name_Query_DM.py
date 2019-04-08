
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

class Image_Name_Query_DM(Request):
    def __init__(self,
                 **kwargs):
        super(Image_Name_Query_DM, self).__init__(**kwargs)

        # Response values
        self._image_name_array = []

    @property
    def image_name_array(self):
        return self._image_name_array

    @image_name_array.setter
    def image_name_array(self, value):
        self._image_name_array = value

    def unpack(self, buf):
        offset = 0

        # image_name_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # image_name_array
        while alen > 0:
            entry = Obj()
            self._image_name_array.append(entry)

            # image_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # image_name (string,1-8,char42)
            entry.image_name = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen

            alen -= (nlen + 4)

