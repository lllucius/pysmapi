
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

class Profile_Replace_DM(Request):
    def __init__(self,
                 profile_record_array = [],
                 **kwargs):
        super(Profile_Replace_DM, self).__init__(**kwargs)

        # Request parameters
        self._profile_record_array = profile_record_array

    @property
    def profile_record_array(self):
        return self._prototype_name

    @profile_record_array.setter
    def profile_record_array(self, value):
        self._profile_record_array = value

    def pack(self):
        alen = 0
        buf = ""
        for profile_record in self._profile_record_array:
            ir_len = len(profile_record)

            # profile_record_length (int4)
            # profile_record (string,1-72,charNA)
            fmt = "!I%ds" % (ir_len)
            buf += struct.pack(fmt,
                               ir_len,
                               bytes(profile_record, "UTF-8"))
            alen += ir_len + 4

        # profile_record_array_length (int4)
        # profile_record_array
        buf = struct.pack(alen) + buf

        return buf
