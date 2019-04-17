
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

class VMRM_Measurement_Query(Request):
    def __init__(self,
                 **kwargs):
        super(VMRM_Measurement_Query, self).__init__(**kwargs)

        # Response values
        self._query_timestamp = ""
        self._file_spec = ""
        self._file_timestamp = ""
        self._workload_array = []

    @property
    def query_timestamp(self):
        return self._query_timestamp

    @query_timestamp.setter
    def query_timestamp(self, value):
        self._query_timestamp = value

    @property
    def file_spec(self):
        return self._file_spec

    @file_spec.setter
    def file_spec(self, value):
        self._file_spec = value

    @property
    def file_timestamp(self):
        return self._file_timestamp

    @file_timestamp.setter
    def file_timestamp(self, value):
        self._file_timestamp = value

    @property
    def workload_array(self):
        return self._workload_array

    @workload_array.setter
    def workload_array(self, value):
        self._workload_array = value

    def unpack(self, buf):
        offset = 0

        # query_timestamp_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # query_timestamp (string,1-17,char42)
        self._query_timestamp = b2s(buf[offset:offset + alen])
        offset += alen

        # file_spec_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # file_spec (string,1-17,char42)
        self._file_spec = b2s(buf[offset:offset + alen])
        offset += alen

        # file_timestamp_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        # file_timestamp (string,1-17,char42)
        self._file_timestamp = b2s(buf[offset:offset + alen])
        offset += alen

        # workload_array_length (int4)
        alen, = struct.unpack("!I", buf[offset:offset + 4])
        offset += 4

        self._workload_array = []
        while alen > 0:
            entry = Obj()
            self._workload_array.append(entry)
            
            # workload_length (int4)
            slen, = struct.unpack("!I", buf[offset:offset + 4])
            offset += 4
            alen -= 4

            # workload (string,1-35,charNA)
            entry.workload, \
            _, \
            entry.cpu, \
            _, \
            entry.dasd = b2s(buf[offset:offset + slen]).split()
            offset += slen
            alen -= slen

