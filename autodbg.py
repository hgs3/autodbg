#!/usr/bin/env python
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

import socket, time, sys, readline

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
CONTINUE_CMD = 'cont'

# Open our remote debugger.
debugger_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
debugger_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
debugger_socket.bind((TCP_IP, TCP_PORT))
debugger_socket.listen(1)

print('Debugger started, waiting for JavaScript to call eval(breakpoint())...')

connection = None
try:
    while 1:
        # Block until the user connects to us.
        connection, address = debugger_socket.accept()

        # Get the result of our last command and breakpoint name.
        result = connection.recv(BUFFER_SIZE)

        # Split on first occurance of \n only.  This is because breakpoint name
        # might have a \n in it.
        result = result.split('\n',1)
        previous_result = result[0]
        breakpoint_name = result[1]

        # Write the result of our last command.
        if previous_result != "'undefined'": print(previous_result)

        # Let the user enter some code to execute.
        while 1:
            debug_command = raw_input('(' + breakpoint_name + ') > ')
            if debug_command != 'help':
                break
            # The user entered the 'help' command.
            print('Help:')
            print(' cont - Continues execution of your test.')
            print(' help - The message your seeing now.')

        # If they entered a "continue" command, log it.
        if debug_command == CONTINUE_CMD:
            print("\nContinuing test, waiting for JavaScript to call eval(breakpoint())...")

        # Send the command to our debug frame.
        connection.send(debug_command)

except KeyboardInterrupt:
    # If they CTRL+C'd our debugger, catch it, and let the debug frame know.
    if connection: connection.send(CONTINUE_CMD)

finally:
    # Make sure we cleanup after ourselves.
    if connection: connection.close()
    debugger_socket.close()

