
# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required domain_name applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct

from pysmapi.smapi import *

class VMRELOCATE_Image_Attributes(Request):
    def __init__(self,
                 relocation_setting = "",
                 domain_name = "",
                 archforce = "",
                 **kwargs):
        super(VMRELOCATE_Image_Attributes, self).__init__(**kwargs)

        # Request parameters
        self._relocation_setting = relocation_setting
        self._domain_name = domain_name
        self._archforce = archforce

    @property
    def relocation_setting(self):
        return self._relocation_setting

    @relocation_setting.setter
    def relocation_setting(self, value):
        self._relocation_setting = value

    @property
    def domain_name(self):
        return self._domain_name

    @domain_name.setter
    def domain_name(self, value):
        self._domain_name = value

    @property
    def archforce(self):
        return self._archforce

    @archforce.setter
    def archforce(self, value):
        self._archforce = value

    def pack(self):
        buf = ""

        # relocation_setting=value (string,2-3,char26)
        buf += f"relocation_setting={self._relocation_setting}\x00"

        # domain_name=value (string,0-8,char42)
        if len(self._domain_name) > 0:
            buf += f"domain_name={self._domain_name}\x00"

        # archforce=value (string,0-3,char26)
        if len(self._archforce) > 0:
            buf += f"archforce={self._archforce}\x00"

        return s2b(buf)

