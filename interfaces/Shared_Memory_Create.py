
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

class Shared_Memory_Create(Request):

    # Page access descriptor
    SW = 1
    EW = 2
    SR = 3
    ER = 4
    SN = 5
    EN = 6
    SC = 7
    page_access_descriptor_names = ["SC"]

    # Memory attributes
    UNSPECIFIED = 0
    RSTD = 1
    UNRSTD = 2
    memory_attributes_names = ["UNRSTD"]
    
    def __init__(self,
                 memory_segment_name = 0,
                 begin_page = "",
                 end_page = "",
                 page_access_descriptor = 0,
                 memory_attributes = 0,
                 memory_access_identifier = "",
                 **kwargs):
        super(Shared_Memory_Create, self).__init__(**kwargs)

        # Request parameters
        self._memory_segment_name = memory_segment_name
        self._begin_page = begin_page
        self._end_page = end_page
        self._page_access_descriptor = page_access_descriptor
        self._memory_attributes = memory_attributes
        self._memory_access_identifier = memory_access_identifier

    @property
    def memory_segment_name(self):
        return self._memory_segment_name

    @memory_segment_name.setter
    def memory_segment_name(self, value):
        self._memory_segment_name = value

    @property
    def begin_page(self):
        return self._begin_page

    @begin_page.setter
    def begin_page(self, value):
        self._begin_page = value

    @property
    def end_page(self):
        return self._end_page

    @end_page.setter
    def end_page(self, value):
        self._end_page = value

    @property
    def page_access_descriptor(self):
        return self._page_access_descriptor

    @page_access_descriptor.setter
    def page_access_descriptor(self, value):
        self._page_access_descriptor = value

    @property
    def memory_attributes(self):
        return self._memory_attributes

    @memory_attributes.setter
    def memory_attributes(self, value):
        self._memory_attributes = value

    @property
    def memory_access_identifier(self):
        return self._memory_access_identifier

    @memory_access_identifier.setter
    def memory_access_identifier(self, value):
        self._memory_access_identifier = value

    def pack(self):
        msn_len = len(self._memory_segment_name)
        mai_len = len(self._memory_access_identifier)

        # memory_segment_name_length (int4)
        # memory_segment_name (string,1-8,char42)
        # begin_page (int8; range 0-524031)
        # end_page (int8; range 0-524031)
        # page_access_descriptor (int1)
        # memory_attributes (int1)
        # memory_access_identifier_length (int4)
        # memory_access_identifier (string,0-8,char42)
        fmt = "!I%dsQQBBI%ds" % \
            (msn_len,
             mai_len)

        buf = struct.pack(fmt,
                          msn_len,
                          bytes(self._memory_segment_name, "UTF-8"),
                          self._begin_page,
                          self._end_page,
                          self._page_access_descriptor,
                          self._memory_attributes,
                          mai_len,
                          bytes(self._memory_access_identifier, "UTF-8"))

        return buf
