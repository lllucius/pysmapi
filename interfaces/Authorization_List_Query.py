
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

class Authorization_List_Query(Request):
    def __init__(self,
                 for_id = "=",
                 function_id = "",
                 **kwargs):
        super(Authorization_List_Query, self).__init__(**kwargs)

        # Request parameters
        self._for_id = for_id
        self._function_id = function_id

        # Response values
        self._auth_record_array = []

    @property
    def for_id(self):
        return self._for_id

    @for_id.setter
    def for_id(self, value):
        self._for_id = value

    @property
    def function_id(self):
        return self._function_id

    @function_id.setter
    def function_id(self, value):
        self._function_id = value

    @property
    def auth_record_array(self):
        return self._auth_record_array

    @auth_record_array.setter
    def auth_record_array(self, value):
        self._auth_record_array = value

    def pack(self):
        for_len = len(self._for_id)
        func_len = len(self.function_id)

        # for_id_length (int4)
        # for_id (string,0-8,char42)
        #        (string,0-64,char43)
        #        (string,1,=)
        #        (string,1,*)
        # function_id_length (int4)
        # function_id (string,0-64,char43)
        #             (string,1,*)
        fmt = "!I%dsI%ds" % (for_len, func_len)
        buf = struct.pack(fmt,
                          for_len,
                          bytes(self._for_id, "UTF-8"),
                          func_len,
                          bytes(self._function_id, "UTF-8"))
 
        return buf
        
    def unpack(self, buf):
        offset = 0

        # auth_record_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._auth_record_array = []
        while alen > 0:
            entry = Obj()
            self._auth_record_array.append(entry)

            # auth_record_structure_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # requesting_userid_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # requesting_userid (string,1-8,char42)
            #                   (string,1-64,char43)
            entry.requesting_userid = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen

            # requesting_list_indicator (int1)
            entry.requesting_list_indicator = buf[offset]
            offset += 1

            # for_userid_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # for_userid (string,1-8,char42)
            #            (string,1-64,char43)
            entry.for_userid = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen

            # for_list_indicator (int1)
            entry.for_list_indicator = buf[offset]
            offset += 1

            # function_name_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # function_name (string,1-64,char43)
            entry.function_userid = buf[offset:offset + nlen].decode("UTF-8")
            offset += nlen

            # function_list_indicator (int1)
            entry.function_list_indicator = buf[offset]
            offset += 1

