
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

class Asynchronous_Notification_Disable_DM(Request):

    # Entity type
    DIRECTORY = 1
    entity_type_names = ["DIRECTORY"]

    # Communication type
    TCP = 1
    UDP = 2
    communication_type_names = ["UDP"]

    # Encoding
    UNSPECIFIED = 0
    ASCII = 1
    EBCDIC = 2
    encoding_names = ["EBCDIC"]

    def __init__(self,
                 entity_type = DIRECTORY,
                 communication_type = TCP,
                 port_number = 0,
                 ip_address = "",
                 encoding = UNSPECIFIED,
                 subscriber_data = "",
                 **kwargs):
        super(Asynchronous_Notification_Disable_DM, self).__init__(**kwargs)

        # Request parameters
        self._entity_type = entity_type
        self._communication_type = communication_type
        self._port_number = port_number
        self._ip_address = ip_address
        self._encoding = encoding
        self._subscriber_data = subscriber_data

    @property
    def entity_type(self):
        return self._entity_type

    @entity_type.setter
    def entity_type(self, value):
        self._entity_type = value

    @property
    def communication_type(self):
        return self._communication_type

    @communication_type.setter
    def communication_type(self, value):
        self._communication_type = value

    @property
    def port_number(self):
        return self._port_number

    @port_number.setter
    def port_number(self, value):
        self._port_number = value

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        self._encoding = value

    @property
    def subscriber_data(self):
        return self._subscriber_data

    @subscriber_data.setter
    def subscriber_data(self, value):
        self._subscriber_data = value

    def pack(self):
        ip_len = len(self._ip_address)
        sub_len = len(self._subscriber_data)

        # entity_type (int1)
        # communication_type (int1)
        # port_number (int4; range 0-65535)
        # ip_address_length (int4)
        # ip_address (string,7-15,char10 plus .)
        # encoding (int1)
        # subscriber_data_length (int4)
        # subscriber_data (string,0-64,charNA)
        #                 (string,1,*)
        fmt = "!BBII%dsBI%ds" % (ip_len, sub_len)
        buf = struct.pack(fmt,
                          self._entity_type,
                          self._communication_type,
                          self._port_number,
                          ip_len,
                          bytes(self._ip_address, "UTF-8"),
                          self._encoding,
                          sub_len,
                          bytes(self._subscriber_data, "UTF-8"))
 
        return buf

