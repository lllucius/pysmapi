
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

class Image_Password_Set_DM(Smapi_Request_Base):
    def __init__(self,
                 image_password = b"",
                 **kwargs):
        super(Image_Password_Set_DM, self). \
            __init__(b"Image_Password_Set_DM", **kwargs)

        # Request parameters
        self._image_password = image_password

    @property
    def image_password(self):
        return self._image_password

    @image_password.setter
    def image_password(self, value):
        self._image_password = value

    def pack(self):
        ip_len = len(self._image_password)

        # image_password_length (int4)
        # image_password (string,1-200,charNA)
        fmt = b"!I%ds" % (ip_len)

        buf = struct.pack(fmt,
                          ip_len,
                          self._image_password)
 
        return super(Image_Password_Set_DM, self).pack(buf)

