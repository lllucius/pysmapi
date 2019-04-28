
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

class System_Info_Query(Request):
    def __init__(self,
                 **kwargs):
        super(System_Info_Query, self).__init__(**kwargs)

        # Response values
        self._time_zone = ""
        self._date_time = ""
        self._cp_level = ""
        self._gen_date_time = ""
        self._ipl_date_time = ""
        self._storage_info = ""

    @property
    def monrate(self):
        return self._monrate

    @monrate.setter
    def monrate(self, value):
        self._monrate = value

    @property
    def time_zone(self):
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value):
        self._time_zone = value

    @property
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, value):
        self._date_time = value

    @property
    def cp_level(self):
        return self._cp_level

    @cp_level.setter
    def cp_level(self, value):
        self._cp_level = value

    @property
    def gen_date_time(self):
        return self._gen_date_time

    @gen_date_time.setter
    def gen_date_time(self, value):
        self._gen_date_time = value

    @property
    def ipl_date_time(self):
        return self._ipl_date_time

    @ipl_date_time.setter
    def ipl_date_time(self, value):
        self._ipl_date_time = value

    @property
    def storage_info(self):
        return self._storage_info

    @storage_info.setter
    def storage_info(self, value):
        self._storage_info = value

    def unpack(self, buf):
        fields = b2s(buf[:-1]).split("\x00")

        self._time_zone = fields[0]
        self._date_time = fields[1]
        self._cp_level = fields[2]
        self._gen_date_time = fields[3]
        self._ipl_date_time = fields[4]
        self._storage_info = fields[5]

