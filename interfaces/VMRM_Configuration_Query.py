
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

class VMRM_Configuration_Query(Request):
    def __init__(self,
                 configuration_file_name = "",
                 configuration_file_type = "",
                 configuration_dir_name = "",
                 **kwargs):
        super(VMRM_Configuration_Query, self).__init__(**kwargs)

        # Request parameters
        self._configuration_file_name = configuration_file_name
        self._configuration_file_type = configuration_file_type
        self._configuration_dir_name = configuration_dir_name

        # Response values
        self._configuration_file = []

    @property
    def configuration_file_name(self):
        return self._configuration_file_name

    @configuration_file_name.setter
    def configuration_file_name(self, value):
        self._configuration_file_name = value

    @property
    def configuration_file_type(self):
        return self._configuration_file_type

    @configuration_file_type.setter
    def configuration_file_type(self, value):
        self._configuration_file_type = value

    @property
    def configuration_dir_name(self):
        return self._configuration_dir_name

    @configuration_dir_name.setter
    def configuration_dir_name(self, value):
        self._configuration_dir_name = value

    @property
    def configuration_file(self):
        return self._configuration_file

    @configuration_file.setter
    def configuration_file(self, value):
        self._configuration_file = value

    def pack(self):
        cfn_len = len(self._configuration_file_name)
        cft_len = len(self._configuration_file_type)
        cdn_len = len(self._configuration_dir_name)

        # configuration_file_name_length (int4)
        # configuration_file_name (string,1-8,char43)
        # configuration_file_type_length (int4)
        # configuration_file_type (string,1-8,char43)
        # configuration_dir_name_length (int4)
        # configuration_dir_name (string,1-153,char43 plus .)
        fmt = "!I%dsI%dsI%ds" % \
            (cfn_len,
             cft_len,
             cdn_len)

        buf = struct.pack(fmt,
                          cfn_len,
                          bytes(self._configuration_file_name, "UTF-8"),
                          cft_len,
                          bytes(self._configuration_file_type, "UTF-8"),
                          cdn_len,
                          bytes(self._configuration_dir_name, "UTF-8"))

        return buf

    def unpack(self, buf):
        offset = 0

        # configuration_file_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._configuration_file = buf[offset:].decode("UTF-8").split("\x00")
