
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

class Image_IPL_Set_DM(Request):
    def __init__(self,
                 saved_system = "",
                 load_parameter = "",
                 parameter_string = "",
                 **kwargs):
        super(Image_IPL_Set_DM, self).__init__(**kwargs)

        # Request parameters
        self._saved_system = saved_system
        self._load_parameter = load_parameter
        self._parameter_string = parameter_string

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

    def pack(self):
        ss_len = len(self._saved_system)
        lp_len = len(self._load_parameter)
        ps_len = len(self._parameter_string)

        # saved_system_length (int4)
        # saved_system (string,1-8,char42)
        # load_parameter_length (int4)
        # load_parameter (string,0-10,char)
        # parameter_string_length (int4)
        # parameter_string (string,0-64,char)
        fmt = "!I%dsI%dsI%ds" % \
            (ss_len,
             lp_len,
             ps_len)

        buf = struct.pack(fmt,
                          ss_len,
                          s2b(self._saved_system),
                          lp_len,
                          s2b(self._load_parameter),
                          ps_len,
                          s2b(self._parameter_string))
 
        return buf
