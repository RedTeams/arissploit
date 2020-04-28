#!/usr/bin/env python3

#            ---------------------------------------------------
#                           Arissploit Framework                                 
#            ---------------------------------------------------
#                Copyright (C) <2019-2020>  <Entynetproject>
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.

from core.arissploit import *
from core import colors
import socket
import subprocess
from datetime import datetime

conf = {
	"name": "port_scanner",
	"version": "1.0",
	"shortdesc": "Website ports scanner.",
	"author": "Entynetproject",
	"initdate": "4.3.2019",
	"lastmod": "3.1.2019",
	"apisupport": True
}

# List of the variables
variables = OrderedDict((
	('target', ['google.com', 'Target web address.']),
	('first', [1, 'First port which will be scanned.']),
	('last', [100, 'Last port which will be scanned.']),
))

# Simple changelog
changelog = "Version 1.0:\nrelease"

def run():
	open_ports = []
	variables['target'][0] = variables['target'][0].replace("http://", "")
	variables['target'][0] = variables['target'][0].replace("https://", "")
	try:
		targetip = socket.gethostbyname(variables['target'][0])
	except(socket.gaierror):
		printError('Hostname could not be resolved!')
		return ModuleError("Hostname could not be resolved!")

	socket.setdefaulttimeout(0.5)

	print(colors.blue+"-" * 60)
	print("Please wait, scanning target...", targetip)
	print("-" * 60+colors.end)

	t1 = datetime.now()

	end = variables['last'][0] + 1

	try:
		for port in range(int(variables['first'][0]),int(end)):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((targetip, port))
			if result == 0:
				print(colors.green+"Port {}: Open".format(port)+colors.end)
				open_ports.append(port)
			else:
				print("["+colors.bold+colors.red+"err"+colors.end+"] Port {}: Closed".format(port)+colors.end)

			sock.close()

	except(socket.gaierror):
		printError('Hostname could not be resolved!')
		return ModuleError("Hostname could not be resolved!")
	except(socket.error):
		printError(colors.red+"Couldn't connect to server!"+colors.end)
		return ModuleError("Couldn't connect to server!")
	except(ValueError):
		printError("Port value must be integer!")
		return ModuleError("Port value must be integer!")

	# Checking the time again
	t2 = datetime.now()

	# Calculates the difference of time, to see how long it took to run the script
	total =  t2 - t1

	# Printing the information to screen
	printInfo('Scanning completed in: '+ str(total))
	return open_ports
