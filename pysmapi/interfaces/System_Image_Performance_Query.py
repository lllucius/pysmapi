
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

class System_Image_Performance_Query(Request):
    def __init__(self,
                 **kwargs):
        super(System_Image_Performance_Query, self).__init__(**kwargs)

        # Response values
        self._image_performance_array = []

    @property
    def image_performance_array(self):
        return self._image_performance_array

    @image_performance_array.setter
    def image_performance_array(self, value):
        self._image_performance_array = value

    def unpack(self, buf):
        offset = 0

        # image_performance_array_entries (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # prototype_record_array
        self._image_performance_array = []
        while alen > 0:
            # entry_data_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # entry_data (DIAGNOSE x'2FC')
            self._image_performance_array.append(buf[offset:offset + nlen])
            offset += nlen

            alen -= 1

