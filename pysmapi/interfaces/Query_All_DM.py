
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

class Query_All_DM(Request):
    # Directory entry type
    USER = 0
    PROFILE = 1
    POOLUSER = 2
    POOL = 3
    DIRECTORY = 4
    GLOBAL = 5
    IDENTITY = 6
    SUBCONFIG = 7
    OTHER = 8
    directory_entry_type_names = {USER: "USER", PROFILE: "PROFILE", POOLUSER: "POOLUSER", POOL: "POOL", DIRECTORY: "DIRECTORY", GLOBAL: "GLOBAL", IDENTITY: "IDENTITY", SUBCONFIG: "SUBCONFIG", OTHER: "OTHER"}

    def __init__(self,
                 query_keyword_parameter_list = "",
                 **kwargs):
        super(Query_All_DM, self).__init__(**kwargs)

        # Request parameters
        self._query_keyword_parameter_list = query_keyword_parameter_list

        # Response values
        self._directory_entries_array = []

    @property
    def query_keyword_parameter_list(self):
        return self._query_keyword_parameter_list

    @query_keyword_parameter_list.setter
    def query_keyword_parameter_list(self, value):
        self._query_keyword_parameter_list = value

    @property
    def directory_entries_array(self):
        return self._directory_entries_array

    @directory_entries_array.setter
    def directory_entries_array(self, value):
        self._directory_entries_array = value

    def pack(self, **kwargs):
        pl_len = len(self._query_keyword_parameter_list)

        # query_keyword_parameter_list_length (int4)
        # query_keyword_parameter_list (string,1-maxlength,charNA)
        fmt = "!I%ds" % (pl_len)

        buf = struct.pack(fmt,
                          pl_len,
                          s2b(self._query_keyword_parameter_list))

        return buf

    def unpack(self, buf):
        offset = 0

        # directory_entries_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._directory_entries_array = []
        while alen > 0:
            entry = Obj()
            self._directory_entries_array.append(entry)

            # directory_entry_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # directory_entry_type (int4)
            entry.directory_entry_type, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # directory_entry_id_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # directory_entry_id (string,1-10,charNA)
            entry.directory_entry_id = b2s(buf[offset:offset + nlen])
            offset += nlen

            if self._query_keyword_parameter_list.lower() == "format=yes":
                # directory_entry_data_length (int4)
                nlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                # directory_entry_data (string,1-maxlength,charNA)
                entry.directory_entry_data = b2s(buf[offset:offset + nlen]).split("\x00")
                offset += nlen

            else:
                # directory_entry_data_length (int4)
                dlen, = struct.unpack("!I", buf[offset:offset + 4])
                offset += 4

                entry.directory_entry_data_array = []
                while dlen > 0:
                    dentry = Obj()
                    entry.directory_entry_data_array.append(dentry)

                    # directory_entry_record_length (int4)
                    nlen, = struct.unpack("!I", buf[offset:offset + 4])
                    offset += 4
                    dlen -= (nlen + 4)

                    # directory_entry_record (string,1-80,charNA)
                    dentry.directory_entry_data = b2s(buf[offset:offset + nlen])
                    offset += nlen

