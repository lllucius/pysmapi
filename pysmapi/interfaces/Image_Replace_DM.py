
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

class Image_Replace_DM(Request):
    def __init__(self,
                 image_record_array = [],
                 **kwargs):
        super(Image_Replace_DM, self).__init__(**kwargs)

        # Request parameters
        self._image_record_array = image_record_array

    @property
    def image_record_array(self):
        return self._image_record_array

    @image_record_array.setter
    def image_record_array(self, value):
        self._image_record_array = value

    def pack(self):
        alen = 0
        buf = b""
        for image_record in self._image_record_array:
            ir_len = len(image_record)

            # image_record_length (int4)
            # image_record (string,1-72,charNA)
            fmt = "!I%ds" % (ir_len)
            buf += struct.pack(fmt,
                               ir_len,
                               s2b(image_record))
            alen += ir_len + 4

        # image_record_array_length (int4)
        # image_record_array
        buf = struct.pack("!I", alen) + buf

        return buf
