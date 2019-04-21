#!/usr/bin/python3

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

import errno
import fnmatch
import json
import os
import sys

import hexdump
import jsonpickle
import select
import socket
import socketserver
import threading
import traceback

from difflib import unified_diff as unified

import pysmapi as smapi

true = True
false = False
null = None

testhome = "tests"
conn = None
server_thread = None
server = None
ip = None
port = None
request = None
response = None


def set_hostinfo(hinfo):
    global conn

    conn = hinfo
    
def gentest(api, testname, expect=[(0,0)], **kwargs):
    global testhome, conn

    smapi.set_test(True)

    if testname:
       print(f"##### Generating {api} test: {testname}")
    else:
       print(f"##### Executing {api}")

    # Get a reference to the target class
    cls = getattr(globals()["smapi"], api)

    # Create instance using keywords
    try:
        req1 = cls(**kwargs)
    except Exception as e:
        print(f"Creation using keywords failed: {e}")
        traceback.print_exc()
        quit()

    # Create instance using setattr
    try:
        req2 = cls()
    except Exception as e:
        print(f"Creation using setattr failed: {e}")
        traceback.print_exc()
        quit()

    # and set its attributes
    try:
        for key, val in kwargs.items():
            setattr(req2, key, val)
            if getattr(req1, key) != getattr(req2, key):
                print(f"mismatch for: {key}")
                print(f"     keyword: {getattr(req1, key)}")
                print(f"     setattr: {getattr(req2, key)}")
                quit()
    except Exception as e:
        print(f"setting attribute {key} failed: {e}")
        traceback.print_exc()
        quit()

    # Convert the requests to json
    res1 = json.dumps(json.loads(jsonpickle.encode(req1, unpicklable=False)), indent=1)
    res2 = json.dumps(json.loads(jsonpickle.encode(req2, unpicklable=False)), indent=1)

    # Compare the requests to ensure they were created the same
    diff = "\n".join(unified(res1.split("\n"), res2.split("\n"), lineterm=""))
    if len(diff) > 0:
        print(f"Creation different between keyword and setattr methods")
        print(diff)
        quit()

    # Execute request
    try:
        req1.request(conn)
    except Exception as e:
        print(f"Executing keyword method failed: {e}")
        traceback.print_exc()
        quit()

    # Tell somebody that the test MAY not have ended properly
    if (-1, -1) not in expect and \
       (req1._return_code, -1) not in expect and \
       (-1, req1._reason_code) not in expect and \
       (req1._return_code, req1._reason_code) not in expect:
        print(f"##### WARNING: rc={req1._return_code} rs={req1._reason_code}")

    # Convert the post execution request to json
    res = json.dumps(json.loads(jsonpickle.encode(req1, unpicklable=False)), indent=1)

    # Save the results if a testname was provided
    if testname:
        # Generate the path and create the directories if needed
        path = os.path.join(testhome, api)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, testname + ".test")

        # And finally write out the testcase
        with open(path, "w") as f:
            f.write(f"api = '{api}'\n")
            f.write(f"kwargs = {kwargs}\n")
            f.write(f"result = \\\n{res}\n")

    return req1

class TestServer(socketserver.BaseRequestHandler):
    def handle(self):
        global request, response

        # Receive the request
        try:
            received = self.recv(len(request))

            #print("Received:")
            #print(hexdump.hexdump(received, result="return"))

            if received != request:
                print("Received request doesn't match expected")
                print("Expected:")
                print(hexdump.hexdump(request, result="return"))
                print
                print("Received:")
                print(hexdump.hexdump(received, result="return"))
                return
        except Exception as e:
            traceback.print_exc()
            return

        # Make sure there's no more after the request
        try:
            received = self.recv(1)
            print("Unexpected data received after request")
            return True
        except IOError as e:
            if e.errno != errno.ETIMEDOUT:
                traceback.print_exc()
                return

        # Send the response
        self.request.sendall(response)

    def recv(self, length, timeout=1):
        buf = b""

        while length > 0:
            rlist, _, _ = select.select([self.request], [], [], timeout)
            if len(rlist) == 0:
                raise IOError(errno.ETIMEDOUT, f"Timed out waiting to receive {length} bytes")

            read = self.request.recv(length)
            if len(read) == 0:
                raise IOError(errno.ENOTCONN, "Connection closed by remote")

            buf += read
            length -= len(read)

        return buf

def start_server():
    global server_thread, server, ip, port

    server = socketserver.TCPServer(("localhost", 0), TestServer)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    set_hostinfo(smapi.HostInfo(host=ip,
                                port=port,
                                ssl=False,
                                userid="maint",
                                password="maint",
                                timeout=600))


def runtest(path):
    global request, response

    smapi.set_test(True)

    # Extract the test name 
    testname = os.path.splitext(os.path.basename(path))[0]

    # Pull in the test
    testvars = {}
    exec(open(path).read(), globals(), testvars)

    # Copy in the variables
    api = testvars["api"]
    kwargs = testvars["kwargs"]
    result = jsonpickle.decode(json.dumps(testvars["result"]))

    print(f"##### Running {api} test: {testname}")

    # Extract the original request and response
    request = result["_send"]
    response = result["_recv"]

    # Get a reference to the target class
    cls = getattr(globals()["smapi"], api)

    # Create instance using keywords
    try:
        req1 = cls(**kwargs)
    except Exception as e:
        print(f"Creation using keywords failed: {e}")
        traceback.print_exc()
        quit()

    # Create instance using setattr
    try:
        req2 = cls()
    except Exception as e:
        print(f"Creation using setattr failed: {e}")
        traceback.print_exc()
        quit()

    # And set its attributes
    try:
        for key, val in kwargs.items():
            setattr(req2, key, val)
            if getattr(req1, key) != getattr(req2, key):
                print(f"Mismatch for: {key}")
                print(f"     keyword: {getattr(req1, key)}")
                print(f"     setattr: {getattr(req2, key)}")
                quit()
    except Exception as e:
        print(f"Setting attributes failed: {e}")
        traceback.print_exc()
        quit()

    # Convert the requests to json
    res1 = json.dumps(json.loads(jsonpickle.encode(req1, unpicklable=False)), indent=1)
    res2 = json.dumps(json.loads(jsonpickle.encode(req2, unpicklable=False)), indent=1)

    # Compare the requests to ensure they were created the same
    diff = "\n".join(unified(res1.split("\n"), res2.split("\n"), lineterm=""))
    if len(diff) > 0:
        print(f"Creation different between keyword and setattr methods")
        print(diff)
        quit()

    # Execute request
    try:
        req1.request(conn)
    except Exception as e:
        print(f"Test execution failed:: {e}")
        traceback.print_exc()
        quit()

    # Convert the post execution request to json
    res1 = json.dumps(json.loads(jsonpickle.encode(req1, unpicklable=False)), indent=1)

    # Convert the captured result to json
    res2 = json.dumps(json.loads(jsonpickle.encode(result, unpicklable=False)), indent=1)

    # Compare the results to ensure they match
    diff = "\n".join(unified(res1.split("\n"), res2.split("\n"), lineterm=""))
    if len(diff) > 0:
        print(f"Results different between keyword and setattr methods")
        print(diff)
        quit()

