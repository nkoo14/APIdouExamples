import logging
import sys
import time
from apidou import *
import socket
from array import array

sock = ''

def sendScratchCommand(cmd):
	global sock

	s = 'broadcast "' + cmd + '"'
	n = len(s)
	a = array('c')
	a.append(chr((n >> 24) & 0xFF))
	a.append(chr((n >> 16) & 0xFF))
	a.append(chr((n >>  8) & 0xFF))
	a.append(chr(n & 0xFF))
	print s
	sock.send(a.tostring() + s)

def main():
	"""
	Use this main as a template to build your python code
	"""

	global sock
	logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

	try:
		# Create an APIdou object using a BlueGiga adapter
		# and a given MAC address
		apidou = APIdou("bled112", "CB:99:E8:46:1F:46")
		# Connect to this APIdou
		apidou.connect()

		# Make the APIdou vibrate for 100ms to check if connection is ok
		apidou.setVibration(True)
		time.sleep(0.1)
		apidou.setVibration(False)

		# Start the accelerometer and the touch sensor.
		# Warning : Without this, you will receive no data from APIdou
		apidou.setNotifyTouch(True)
		# apidou.setNotifyAccel(True)

		print("Connecting to Scratch...")
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(("127.0.0.1", 42001))
		sock.settimeout(0.1)

		print("Connected!")

		while True:
			if apidou.isTouched(APIdou.LEFT_FOOT):
				sendScratchCommand("pied_gauche")
			if apidou.isTouched(APIdou.RIGHT_FOOT):
				sendScratchCommand("pied_droit")
			if apidou.isTouched(APIdou.LEFT_HAND):
				sendScratchCommand("main_gauche")
			if apidou.isTouched(APIdou.RIGHT_HAND):
				sendScratchCommand("main_droite")
			if apidou.isTouched(APIdou.LEFT_EAR):
				sendScratchCommand("oreille_gauche")
			if apidou.isTouched(APIdou.RIGHT_EAR):
				sendScratchCommand("oreille_droite")
			if apidou.isTouched(APIdou.ANTENNA):
				sendScratchCommand("antenne")
			try:
				data = sock.recv(100)
				if not data:
					pass
				else:
					msg = data.split('"')[1::2][0]
					print msg
					if msg == "vibre":
						apidou.setVibration(True)
					elif msg == "ne_vibre_plus":
						apidou.setVibration(False)
					else:
						print "Unknown message received"
			except socket.timeout:
				pass
			except Exception, e:
				raise e
			time.sleep(0.1)

	except pygatt.exceptions.NotConnectedError:
		print "Could not connect. Check if device is on (program will exit)"
	except KeyboardInterrupt:
		print "\nCtrl-C pressed. Goodbye!"
	except Exception as e:
		print e
	finally:
		apidou.disconnect()

if __name__ == '__main__':
	main()

