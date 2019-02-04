
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

class System_Disk_IO_Query(Smapi_Request_Base):
    def __init__(self,
                 system_disk_io_list = b"",
                 **kwargs):
        super(System_Disk_IO_Query, self). \
            __init__(b"System_Disk_IO_Query", **kwargs)

        # Request parameters
        self._system_disk_io_list = system_disk_io_list

        # Response values
        self._dasd_information = []
        self._error_data = b""

    @property
    def system_disk_io_list(self):
        return self._system_disk_io_list

    @system_disk_io_list.setter
    def system_disk_io_list(self, value):
        self._system_disk_io_list = value

    @property
    def disk_size(self):
        return self._disk_size

    @disk_size.setter
    def disk_size(self, value):
        self._disk_size = value

    @property
    def dasd_information(self):
        return self._dasd_information

    @dasd_information.setter
    def dasd_information(self, value):
        self._dasd_information = value

    @property
    def error_data(self):
        return self._error_data

    @error_data.setter
    def error_data(self, value):
        self._error_data = value

    def pack(self):
        sdil_len = len(self._system_disk_io_list)

        # system_disk_IO_list_length (int4)
        # system_disk_IO_list (string,1-maxlength,char36 plus * blank)
        fmt = b"!I%ds" % (sdil_len)

        buf = struct.pack(fmt,
                          sdil_len,
                          self._system_disk_io_list)
                          
        return super(System_Disk_IO_Query, self).pack(buf)

    def unpack(self, buf, offset):
        offset = super(System_Disk_IO_Query, self).unpack(buf, offset)

        # DASD_information_length (int4)
        # or
        # error_data_length (int4)
        nlen, = struct.unpack(b"!I", buf[offset:offset + 4])
        offset += 4

        # DASD_information (string)
        # or
        # error_data (string)
        buf = buf[offset:offset + nlen]
        offset += nlen

        if self.return_code == 0 and self.reason_code == 0:
            # dasd_information
            self._dasd_information = buf.split(b"\x00")
        else:
            # error_data
            self._error_data = buf

        return offset

