
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

class Image_Create_DM(Request):
    def __init__(self,
                 prototype_name = "",
                 initial_password = "",
                 initial_account_number = "",
                 image_record_array = [],
                 **kwargs):
        super(Image_Create_DM, self).__init__(**kwargs)

        # Request parameters
        self._prototype_name = prototype_name
        self._initial_password = initial_password
        self._initial_account_number = initial_account_number
        self._image_record_array = image_record_array

        # Response values
        self._operation_id = 0

    @property
    def prototype_name(self):
        return self._prototype_name

    @prototype_name.setter
    def prototype_name(self, value):
        self._prototype_name = value

    @property
    def initial_password(self):
        return self._prototype_name

    @initial_password.setter
    def initial_password(self, value):
        self._initial_password = value

    @property
    def initial_account_number(self):
        return self._prototype_name

    @initial_account_number.setter
    def initial_account_number(self, value):
        self._initial_account_number = value

    @property
    def image_record_array(self):
        return self._prototype_name

    @image_record_array.setter
    def image_record_array(self, value):
        self._image_record_array = value

    @property
    def operation_id(self):
        return self._prototype_name

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = value

    def pack(self):
        alen = 0
        buf = ""
        for image_record in self._image_record_array:
            ir_len = len(image_record)

            # image_record_length (int4)
            # image_record (string,1-72,charNA)
            fmt = "!I%ds" % (ir_len)
            buf += struct.pack(fmt,
                               ir_len,
                               bytes(image_record, "UTF-8"))
            alen += ir_len + 4

        pn_len = len(self._prototype_name)
        ip_len = len(self._initial_password)
        ia_len = len(self._initial_account_number)

        # prototype_name_length (int4)
        # prototype_name (string,0-8,char42)
        # initial_password_length (int4)
        # initial_password (string,0-200,charNA)
        # initial_account_number_length (int4)
        # initial_account_number (string,0-8,charNB)
        # image_record_array_length (int4)
        # image_record_array
        fmt = "!I%dsI%dsI%dsI" % (pn_len, ip_len, ia_len)
        buf = struct.pack(fmt,
                          pn_len,
                          bytes(self._prototype_name, "UTF-8"),
                          ip_len,
                          bytes(self._initial_password, "UTF-8"),
                          ia_len,
                          bytes(self._initial_account_number, "UTF-8"),
                          alen) + buf

        return buf

    def unpack(self, buf):
        offset = 0

        # operation_id (int4; range -1-2147483647)
        self._operation_id, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

