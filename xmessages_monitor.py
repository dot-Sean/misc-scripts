#!/usr/bin/python
#
# Copyright (c) 2007-2008 Sebastian Noack
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

import gamin
import threading
from os import system, path, remove, listdir
from time import sleep
from signal import signal, SIGTERM, SIGINT

MESSAGES_DIR = '/var/log/xmessages'

def handle_message(file):
	class HandleMsgThread (threading.Thread):
		def run(self):
			abs_path = path.join(MESSAGES_DIR, file)
			fd = open(abs_path, 'r')
			msg = fd.read()
			fd.close()
			system('xmessage "%s:\n\n%s"' % (file, msg))
			remove(abs_path)
	HandleMsgThread().start()

def messages_dir_callback(file, event):
	if event == gamin.GAMChanged:
		handle_message(file)
		
def signal_handler(sig, stack_frame):
	exit(0)

# Hanle old messages.
for file in listdir(MESSAGES_DIR):
	handle_message(file)

# Setup file monitor.
mon = gamin.WatchMonitor()
mon.watch_directory(MESSAGES_DIR, messages_dir_callback)

# Handle process signals.
signal(SIGTERM, signal_handler)
signal(SIGINT, signal_handler)

# Enter event handling loop.
while True :
	sleep (1)
	mon.handle_events()
