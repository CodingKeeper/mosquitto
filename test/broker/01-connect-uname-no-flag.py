#!/usr/bin/env python

# Test whether a connection is disconnected if it provides a username but the
# username flag is 0.

import inspect, os, sys
# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import struct
import mosq_test

rc = 1
keepalive = 10
connect_packet = mosq_test.gen_connect("connect-uname-test", keepalive=keepalive, username="user")
b = list(struct.unpack("B"*len(connect_packet), connect_packet))
b[9] = 2 # Remove username flag
connect_packet = struct.pack("B"*len(b), *b)

connack_packet = mosq_test.gen_connack(rc=5)

port = mosq_test.get_port()
broker = mosq_test.start_broker(filename=os.path.basename(__file__), port=port)

try:
    sock = mosq_test.do_client_connect(connect_packet, "", port=port)
    sock.close()
    rc = 0
finally:
    broker.terminate()
    broker.wait()
    if rc:
        (stdo, stde) = broker.communicate()
        print(stde)

exit(rc)

