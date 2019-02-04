
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

class Image_IPL_Query_DM(Smapi_Request_Base):
    def __init__(self,
                 **kwargs):
        super(Image_IPL_Query_DM, self). \
            __init__(b"Image_IPL_Query_DM", **kwargs)

        # Response values
        self._saved_system = 0
        self._load_parameter = 0
        self._parameter_string = 0

    @property
    def saved_system(self):
        return self._saved_system

    @saved_system.setter
    def saved_system(self, value):
        self._saved_system = value

    @property
    def load_parameter(self):
        return self._load_parameter

    @load_parameter.setter
    def load_parameter(self, value):
        self._load_parameter = value

    @property
    def parameter_string(self):
        return self._parameter_string

    @parameter_string.setter
    def parameter_string(self, value):
        self._parameter_string = value

    def unpack(self, buf, offset):
        offset = super(Image_IPL_Query_DM, self).unpack(buf, offset)

        # saved_system_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # saved_system (string,0-10,char)
        self._saved_system = buf[offset:offset + nlen]
        offset += nlen

        # load_parameter_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # load_parameter (string,0-10,char)
        self._load_parameter = buf[offset:offset + nlen]
        offset += nlen

        # parameter_string_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # parameter_string (string,0-10,char)
        self._parameter_string = buf[offset:offset + nlen]
        offset += nlen

        return offset
