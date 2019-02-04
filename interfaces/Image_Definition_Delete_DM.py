
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

class Image_Definition_Delete_DM(Smapi_Request_Base):
    def __init__(self,
                 definition_delete_directory_keyword_parameter_list = [],
                 **kwargs):
        super(Image_Definition_Delete_DM, self). \
            __init__(b"Image_Definition_Delete_DM", **kwargs)

        # Request parameters
        self._definition_delete_directory_keyword_parameter_list = definition_delete_directory_keyword_parameter_list

        # Response values
        self.asynch_data = []
        self.error_data = []

    @property
    def definition_delete_directory_keyword_parameter_list(self):
        return self._prototype_name

    @definition_delete_directory_keyword_parameter_list.setter
    def definition_delete_directory_keyword_parameter_list(self, value):
        self._definition_delete_directory_keyword_parameter_list = value

    @property
    def asynch_data(self):
        return self._prototype_name

    @asynch_data.setter
    def asynch_data(self, value):
        self._asynch_data = value

    @property
    def error_data(self):
        return self._prototype_name

    @error_data.setter
    def error_data(self, value):
        self._error_data = value

    def pack(self):
        buf = b""
        for plist in self._definition_delete_directory_keyword_parameter_list:
            buf += plist + b"\x00"

        # definition_delete_directory_keyword_parameter_list_length (int4)
        # definition_delete_directory_keyword_parameter_list
        buf = struct.pack("!I", len(buf)) + buf

        return super(Image_Definition_Delete_DM, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(System_Service_Query, self).unpack(buf, offset)

        # asynch_length (int4)
        # or
        # error_length (int4)
        alen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # asynch_data (string)
        # or
        # error_data (string)
        array = buf[offset:offset + alen].split("\x00")
        offset += alen

        if self.return_code == 592 and self.reason_code == 4:
            self._asynch_data = array
        else:
            self._error_data = array

        offset += alen

