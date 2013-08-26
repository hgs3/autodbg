'''
Copyright (c) 2013 Henry G. Stratmann III

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# This script will be executed every "debug frame".
# A debug frame is created whenever you call "breakpoint()" from JavaScript.
#
# The purpose of this script is to:
#    1) Send our remote debugger the result of the last command.
#    2) Wait until code is entered and sent to us by the remote debugger.
#    3) Write to stdout the code entered into the remote debugger.
#
# This code written to stdout by this script will be eval()'d in JavaScript
# and the result set as the last command.

import socket, sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


# When creating a conection to our remote debugger, we want to first give it
# the result of the last debug command.
#
# There should _always_ be a result.
if len(sys.argv) != 3:
    sys.stderr.write('Expected a previous result and breakpoint name.')
    sys.exit(1)

previous_result = sys.argv[1]
breakpoint_name = sys.argv[2]

try:
    # Open a connection to our remote debugger and send it the result
    # of the previous command.
    debugger_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debugger_socket.connect((TCP_IP, TCP_PORT))
    debugger_socket.send(previous_result + '\n' + breakpoint_name)

    # Block until we get some code from the remote debugger.
    data = debugger_socket.recv(BUFFER_SIZE)

    # Close our socket and write the command we received to stdout.
    debugger_socket.close()
    sys.stdout.write(data)

except Exception as e:
    # If anything goes wrong e.g. couldn't connect to the debugger,
    # lets report it to JavaScript.
    sys.stderr.write(str(e))
    sys.exit(1)
