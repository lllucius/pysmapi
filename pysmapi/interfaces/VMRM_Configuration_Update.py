
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

class VMRM_Configuration_Update(Request):
    def __init__(self,
                 configuration_file_name = "",
                 configuration_file_type = "",
                 configuration_dir_name = "",
                 syncheck_only = True,
                 update_file = [],
                 **kwargs):
        super(VMRM_Configuration_Update, self).__init__(**kwargs)

        # Request parameters
        self._configuration_file_name = configuration_file_name
        self._configuration_file_type = configuration_file_type
        self._configuration_dir_name = configuration_dir_name
        self._syncheck_only = syncheck_only
        self._update_file = update_file

        # Response values
        self._log_record_array = []

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
    def syncheck_only(self):
        return self._syncheck_only

    @syncheck_only.setter
    def syncheck_only(self, value):
        self._syncheck_only = value

    @property
    def update_file(self):
        return self._update_file

    @update_file.setter
    def update_file(self, value):
        self._update_file = value

    @property
    def log_record_array(self):
        return self._log_record_array

    @log_record_array.setter
    def log_record_array(self, value):
        self._log_record_array = value


    def pack(self):
        buf = "\x00".join(self._update_file)

        cfn_len = len(self._configuration_file_name)
        cft_len = len(self._configuration_file_type)
        cdn_len = len(self._configuration_dir_name)
        uf_len = len(buf)

        # configuration_file_name_length (int4)
        # configuration_file_name (string,1-8,char43)
        # configuration_file_type_length (int4)
        # configuration_file_type (string,1-8,char43)
        # configuration_dir_name_length (int4)
        # configuration_dir_name (string,1-153,char43 plus .)
        fmt = "!I%dsI%dsI%dsBI%ds" % \
            (cfn_len,
             cft_len,
             cdn_len,
             uf_len)

        buf = struct.pack(fmt,
                          cfn_len,
                          s2b(self._configuration_file_name),
                          cft_len,
                          s2b(self._configuration_file_type),
                          cdn_len,
                          s2b(self._configuration_dir_name),
                          self._syncheck_only,
                          uf_len,
                          s2b(buf))

        return buf

    def unpack(self, buf):
        offset = 0

        # log_record_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._log_record_array = []
        while alen > 0:
            # log_record_array_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= 4

            # log_record (string,1-maxlength,charNA)
            self._log_record_array.append(b2s(buf[offset:offset + slen]))
            offset += slen
            alen -= slen
