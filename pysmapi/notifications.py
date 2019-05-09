
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

import socket
import struct
import threading

import pysmapi as smapi

# ==============================================================================
# 
# ==============================================================================
class Notifications(threading.Thread):
    def __init__(self, hostinfo, ip, port=0, include=["ALL"], exclude=[], data=""):
        super().__init__()

        # Kill the thread if process terminates
        self.daemon = True

        self._hostinfo = hostinfo
        self._ip = ip
        self._port = port
        self._include = include
        self._exclude = exclude
        self._data = data

        self._socket = None
        self._shutdown = False
        self._enabled = True
        self._update_handler = self.update

    def set_update_handler(self, handler):
        self._update_handler = handler

    def stop(self):
        self.disable(self._ip, self._port, self._data)

        self._shutdown = True

        skt = socket.create_connection((self._ip, self._port))
        if skt:
            try:
                skt.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                skt.close()
 
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            skt.close()

    def run(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._ip, self._port))
        self._socket.listen(10)

        self._ip, self._port = self._socket.getsockname()

        self.enable(self._ip, self._port, self._data)

        try:
            while True:
                client, address = self._socket.accept()
                if self._shutdown:
                    break

                userid = self.get_data(client)
                user_word = self.get_data(client)
                sub_data = self.get_data(client)

                self._update_handler(userid, user_word, sub_data)
        finally:
            self.disable(self._ip, self._port, self._data)

    def enable(self, host, port, data):
        self._enabled = True

        req = smapi.Asynchronous_Notification_Enable_DM()
        req.entity_type = req.DIRECTORY
        req.communication_type = req.TCP
        req.ip_address = host
        req.port_number = port
        req.subscriber_data = data
        req.encoding = req.ASCII

        try:
            for target in self._include:
                req.subscription_type = req.INCLUDE
                req.target = target
                req.request(self._hostinfo)
                if req.failed():
                    raise Exception(req.error_string())

            for target in self._exclude:
                req.subscription_type = req.EXCLUDE
                req.target = target
                req.request(self._hostinfo)
                if req.failed():
                    raise Exception(req.error_string())
        except:
            self.disable(host, port, data)
            raise

    def disable(self, host, port, data):
        if self._enabled:
            self._enabled = False

            req = smapi.Asynchronous_Notification_Disable_DM()
            req.entity_type = req.DIRECTORY
            req.communication_type = req.TCP
            req.ip_address = host
            req.port_number = port
            req.subscriber_data = data
            req.encoding = req.ASCII

            for target in self._include:
                req.target = target
                req.request(self._hostinfo)

            for target in self._exclude:
                req.target = target
                req.request(self._hostinfo)

    def get_data(self, client):
        length, = struct.unpack("!I", client.recv(4))
        data = bytes()
        while length > 0:
            received = client.recv(length)
            length -= len(received)
            data += received

        return data

    def update(self, user_id, user_word, sub_data):
        pass

