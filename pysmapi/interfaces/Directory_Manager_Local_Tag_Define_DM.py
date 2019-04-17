
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

class Directory_Manager_Local_Tag_Define_DM(Request):
    # Define action
    CREATE = 1
    CHANGE = 2
    define_action_names = {CREATE: "CREATE", CHANGE: "CHANGE"}

    def __init__(self,
                 tag_name = "",
                 tag_ordinal = 0,
                 define_action = CREATE,
                 **kwargs):
        super(Directory_Manager_Local_Tag_Define_DM, self).__init__(**kwargs)

        # Request parameters
        self._tag_name = tag_name
        self._tag_ordinal = tag_ordinal
        self._define_action = define_action

    @property
    def tag_name(self):
        return self._tag_name

    @tag_name.setter
    def tag_name(self, value):
        self._tag_name = value

    @property
    def tag_ordinal(self):
        return self._tag_ordinal

    @tag_ordinal.setter
    def tag_ordinal(self, value):
        self._tag_ordinal = value

    @property
    def define_action(self):
        return self._define_action

    @define_action.setter
    def define_action(self, value):
        self._define_action = value

    def pack(self):
        tn_len = len(self._tag_name)

        # tag_name_length (int4)
        # tag_name (string,1-8,char36)
        # tag_ordinal (int4; range 0-999)
        # define_action (int1)
        fmt = "!I%dsIB" % (tn_len)
        buf = struct.pack(fmt,
                          tn_len,
                          s2b(self._tag_name),
                          self._tag_ordinal,
                          self._define_action)

        return buf

