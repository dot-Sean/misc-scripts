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

from os import system, path, getpid, kill, remove
from optparse import OptionParser

import gobject

import dbus
import dbus.mainloop.glib

def nm_device_now_active_handler(_):
	#gobject.timeout_add(0, loop.quit)
	loop.quit()

if __name__ == '__main__':
	# Parse commandline arguments.
	usage = "Usage: %prog [-p pid_file] <command>"
	parser = OptionParser(usage)
	parser.add_option("-p", dest="pid_file",
		help="If specified the given pid file will be crated. If it already exists it will try to kill the process with the id in it first.")
	(options, args) = parser.parse_args()
	if len(args) != 1 :
		parser.error("incorrect number of arguments")
	
	# Create pid file and try to kill the already running instance of this
	# script if so.
	pid_file = options.pid_file
	if pid_file :
		if path.isfile(pid_file) :
			fd = open(pid_file, 'r+')
			pid = int(fd.read())
			try:
				kill(pid, 15)
			except:
				pass
			fd.seek(0)
		else :
			fd = open(pid_file, 'w')
		fd.write(str(getpid()))
		fd.truncate()
		fd.close()

	# Check if network is connected and wait until it is, if it isn't connected.
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()
	nm = bus.get_object('org.freedesktop.NetworkManager',
						'/org/freedesktop/NetworkManager')
	state = nm.state(dbus_interface='org.freedesktop.NetworkManager')
	if state != 3 :
		nm.connect_to_signal('DeviceNowActive', nm_device_now_active_handler,
		                     dbus_interface='org.freedesktop.NetworkManager')
		loop = gobject.MainLoop()
		loop.run()

	system(args[0])

	# Remove pid file, when script finishes.
	if pid_file :
		remove(pid_file)
