
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

class Image_Query_Activate_Time(Smapi_Request_Base):

    # Date format indicator
    MMDDYY = 1
    MMDDYYYY = 2
    YYMMDD = 3
    YYYYMMDD = 4
    DDMMYY = 5
    DDMMYYYY = 6

    def __init__(self,
                 date_format_indicator = 0,
                 **kwargs):
        super(Image_Query_Activate_Time, self). \
            __init__(b"Image_Query_Activate_Time", **kwargs)

        # Request parameters
        self._date_format_indicator = date_format_indicator

        # Response values
        self._image_name = b""
        self._activation_date = b""
        self._activation_time = b""

    @property
    def date_format_indicator(self):
        return self._date_format_indicator

    @date_format_indicator.setter
    def date_format_indicator(self, value):
        self._date_format_indicator = value

    @property
    def image_name(self):
        return self._image_name

    @image_name.setter
    def image_name(self, value):
        self._image_name = value

    @property
    def activation_date(self):
        return self._activation_date

    @activation_date.setter
    def activation_date(self, value):
        self._activation_date = value

    @property
    def activation_time(self):
        return self._activation_time

    @activation_time.setter
    def activation_time(self, value):
        self._activation_time = value

    def pack(self):
        # date_format_indicator (int1)
        buf = struct.pack("B", self._date_format_indicator)

        return super(Image_Query_Activate_Time, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(Image_Query_Activate_Time, self).unpack(buf, offset)

        # image_name_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # image_name (string,1-8,char42)
        self._image_name = buf[offset:offset + nlen]
        offset += nlen

        # activation_date_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # activation_date (string,8-10,char)
        self._activation_date = buf[offset:offset + nlen]
        offset += nlen

        # activation_time_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # activation_time (string,8,char)
        self._activation_time = buf[offset:offset + nlen]
        offset += nlen

        return offset
