
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

from base import Smapi_Request_Base, Obj

class Asynchronous_Notification_Query_DM(Smapi_Request_Base):

    # Entity type
    DIRECTORY = 1
    entity_type_names = ["?", "DIRECTORY"]

    # Subscription type
    INCLUDE = 1
    EXCLUDE = 2
    subscription_type_names = ["?", "INCLUDE", "EXCLUDE"]

    # Communication type
    TCP = 1
    UDP = 2
    communication_type_names = ["?", "TCP", "UDP"]

    # Encoding
    UNSPECIFIED = 0
    ASCII = 1
    EBCDIC = 2
    encoding_names = ["UNSPECIFIED", "ASCII", "EBCDIC"]

    def __init__(self,
                 entity_type = DIRECTORY,
                 communication_type = UNSPECIFIED,
                 port_number = 0,
                 ip_address = b"",
                 encoding = UNSPECIFIED,
                 subscriber_data = b"",
                 **kwargs):
        super(Asynchronous_Notification_Query_DM, self). \
            __init__(b"Asynchronous_Notification_Query_DM", **kwargs)

        # Request parameters
        self._entity_type = entity_type
        self._communication_type = communication_type
        self._port_number = port_number
        self._ip_address = ip_address
        self._encoding = encoding
        self._subscriber_data = subscriber_data

        # Response values
        self._notification_array = []

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

    @property
    def notification_array(self):
        return self._notification_array

    @notification_array.setter
    def notification_array(self, value):
        self._notification_array = value

    def pack(self):
        ip_len = len(self._ip_address)
        sub_len = len(self._subscriber_data)

        # entity_type (int1)
        # communication_type (int1)
        # port_number (int4; range 0-65535)
        # ip_address_length (int4)
        # ip_address (string,0-15,char10 plus .)
        # encoding (int1)
        # subscriber_data_length (int4)
        # subscriber_data (string,0-64,charNA)
        #                 (string,1,*)
        fmt = b"!BBII%dsBI%ds" % (ip_len, sub_len)
        buf = struct.pack(fmt,
                          self._entity_type,
                          self._communication_type,
                          self._port_number,
                          ip_len,
                          self._ip_address,
                          self._encoding,
                          sub_len,
                          self._subscriber_data)
 
        return super(Asynchronous_Notification_Query_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Asynchronous_Notification_Query_DM, self).unpack(buf, offset)

        # notification_array_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        self._notification_array = []
        while alen > 0:
            entry = Obj()
            self._notification_array.append(entry)

            # notification_structure_length (int4)
            slen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4
            alen -= (slen + 4)

            # userid_length (int4)
            nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # userid (string,1-8,char42)
            entry.userid = buf[offset:offset + nlen]
            offset += nlen

            # subscription_type (int1)
            entry.subscription_type = ord(buf[offset])
            offset += 1

            # communication_type (int1)
            entry.communication_type = ord(buf[offset])
            offset += 1

            # port_number (int4)
            entry.port_number, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # ip_address_length (int4)
            nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
            offset += 4

            # ip_address (string,7-15,char10 plus .)
            entry.ip_address = buf[offset:offset + nlen]
            offset += nlen

            # encoding (int1)
            entry.encoding = ord(buf[offset])
            offset += 1

            # subscriber_data_length (int4)
            nlen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4

            # subscriber_data (string,0-64,charNA)
            entry.subscriber_data = buf[offset:offset + nlen]
            offset += nlen

        return offset

