
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

class Check_Authentication(Request):
    def __init__(self,
                 **kwargs):
        super(Check_Authentication, self).__init__(**kwargs)

    # Override base method entirely since this is the only API that
    # doesn't conform to the standard set of parameters.
    def pack(self):
        fn_len = len(self._function_name)
        au_len = len(self._authenticated_userid)
        p_len = len(self._password)

        # function_name_length (int4)
        # function_name (string,20,char43)
        # authenticated_userid_length (int4)
        # authenticated_userid (string,1-8,char42)
        #                      (string,0-8,char42)
        # password_length (int4)
        # password (string,1-200,charNA)
        #          (string,0-200,charNA)
        fmt = "!I%dsI%dsI%ds" % (fn_len, au_len, p_len)
        buf = struct.pack(fmt,
                          fn_len,
                          bytes(self._function_name, "UTF-8"),
                          au_len,
                          bytes(self._authenticated_userid, "UTF-8"),
                          p_len,
                          bytes(self._password, "UTF-8"))

        # input_length (int4)
        return struct.pack("!I", len(buf)) + buf
