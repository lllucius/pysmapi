
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

class Image_Volume_Delete(Smapi_Request_Base):
    def __init__(self,
                 image_device_number = b"",
                 image_vol_id = b"",
                 system_config_name = b"",
                 system_config_type = b"",
                 parm_disk_owner = b"",
                 parm_disk_number = b"",
                 parm_disk_password = b"",
                 alt_system_config_name = b"",
                 alt_system_config_type = b"",
                 alt_parm_disk_owner = b"",
                 alt_parm_disk_number = b"",
                 alt_parm_disk_password = b"",
                 **kwargs):
        super(Image_Volume_Delete, self). \
            __init__(b"Image_Volume_Delete", **kwargs)

        # Request parameters
        self._image_device_number = image_device_number
        self._image_vol_id = image_vol_id
        self._system_config_name = system_config_name
        self._system_config_type = system_config_type
        self._parm_disk_owner = parm_disk_owner
        self._parm_disk_number = parm_disk_number
        self._parm_disk_password = parm_disk_password
        self._alt_system_config_name = alt_system_config_name
        self._alt_system_config_type = alt_system_config_type
        self._alt_parm_disk_owner = alt_parm_disk_owner
        self._alt_parm_disk_number = alt_parm_disk_number
        self._alt_parm_disk_password = alt_parm_disk_password

    @property
    def image_device_number(self):
        return self._image_device_number

    @image_device_number.setter
    def image_device_number(self, value):
        self._image_device_number = value

    @property
    def image_vol_id(self):
        return self._image_vol_id

    @image_vol_id.setter
    def image_vol_id(self, value):
        self._image_vol_id = value

    @property
    def system_config_name(self):
        return self._system_config_name

    @system_config_name.setter
    def system_config_name(self, value):
        self._system_config_name = value

    @property
    def system_config_type(self):
        return self._system_config_type

    @system_config_type.setter
    def system_config_type(self, value):
        self._system_config_type = value

    @property
    def parm_disk_owner(self):
        return self._parm_disk_owner

    @parm_disk_owner.setter
    def parm_disk_owner(self, value):
        self._parm_disk_owner = value

    @property
    def parm_disk_number(self):
        return self._parm_disk_number

    @parm_disk_number.setter
    def parm_disk_number(self, value):
        self._parm_disk_number = value

    @property
    def parm_disk_password(self):
        return self._parm_disk_password

    @parm_disk_password.setter
    def parm_disk_password(self, value):
        self._parm_disk_password = value

    @property
    def alt_system_config_name(self):
        return self._alt_system_config_name

    @alt_system_config_name.setter
    def alt_system_config_name(self, value):
        self._alt_system_config_name = value

    @property
    def alt_system_config_type(self):
        return self._alt_system_config_type

    @alt_system_config_type.setter
    def alt_system_config_type(self, value):
        self._alt_system_config_type = value

    @property
    def alt_parm_disk_owner(self):
        return self._alt_parm_disk_owner

    @alt_parm_disk_owner.setter
    def alt_parm_disk_owner(self, value):
        self._alt_parm_disk_owner = value

    @property
    def alt_parm_disk_number(self):
        return self._alt_parm_disk_number

    @alt_parm_disk_number.setter
    def alt_parm_disk_number(self, value):
        self._alt_parm_disk_number = value

    @property
    def alt_parm_disk_password(self):
        return self._alt_parm_disk_password

    @alt_parm_disk_password.setter
    def alt_parm_disk_password(self, value):
        self._alt_parm_disk_password = value

    def pack(self):
        idn_len = len(self._image_device_number)
        ivi_len = len(self._image_vol_id)
        scn_len = len(self._system_config_name)
        sct_len = len(self._system_config_type)
        pdo_len = len(self._parm_disk_owner)
        pdn_len = len(self._parm_disk_number)
        pdp_len = len(self._parm_disk_password)
        ascn_len = len(self._alt_system_config_name)
        asct_len = len(self._alt_system_config_type)
        apdo_len = len(self._alt_parm_disk_owner)
        apdn_len = len(self._alt_parm_disk_number)
        apdp_len = len(self._alt_parm_disk_password)

        # image_device_number_length (int4)
        # image_device_number (string,1-4,char16)
        # image_vol_id_length (int4)
        # image_vol_id (string,1-6,char42)
        # system_config_name_length (int4)
        # system_config_name (string,0-8,char42)
        # system_config_type_length (int4)
        # system_config_type (string,0-8,char42)
        # parm_disk_owner_length (int4)
        # parm_disk_owner (string,0-8,char42)
        # parm_disk_number_length (int4)
        # parm_disk_number (string,0-4,char16)
        # parm_disk_password_length (int4)
        # parm_disk_password (string,0-8,charNB)
        # alt_system_config_name_length (int4)
        # alt_system_config_name (string,0-8,char42)
        # alt_system_config_type_length (int4)
        # alt_system_config_type (string,0-8,char42)
        # alt_parm_disk_owner_length (int4)
        # alt_parm_disk_owner (string,0-8,char42)
        # alt_parm_disk_number_length (int4)
        # alt_parm_disk_number (string,0-4,char16)
        # alt_parm_disk_password_length (int4)
        # alt_parm_disk_password (string,0-8,charNB)
        fmt = b"!I%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%dsI%ds" % \
            (idn_len,
             ivi_len,
             scn_len,
             sct_len,
             pdo_len,
             pdn_len,
             pdp_len,
             ascn_len,
             asct_len,
             apdo_len,
             apdn_len,
             apdp_len)

  
        buf = struct.pack(fmt,
                          idn_len,
                          self._image_device_number,
                          ivi_len,
                          self._image_vol_id,
                          scn_len,
                          self._system_config_name,
                          sct_len,
                          self._system_config_type,
                          pdo_len,
                          self._parm_disk_owner,
                          pdn_len,
                          self._parm_disk_number,
                          pdp_len,
                          self._parm_disk_password,
                          ascn_len,
                          self._alt_system_config_name,
                          asct_len,
                          self._alt_system_config_type,
                          apdo_len,
                          self._alt_parm_disk_owner,
                          apdn_len,
                          self._alt_parm_disk_number,
                          apdp_len,
                          self._alt_parm_disk_password)

        return super(Image_Volume_Delete, self).pack(buf)

