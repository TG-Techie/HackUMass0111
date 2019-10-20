# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import random
import cv2
import bitmap



def scan_for_qr():
	"""
	Desc: scans once for a qr code and returns a list of all the codes found;
	"""
	# construct the argument parser and parse the arguments
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	#	help="path to output CSV file containing barcodes")
	#args = vars(ap.parse_args())

	vs = VideoStream(src=0).start()
	#while True:
		# grab the frame from the threaded video stream and resize it to
		# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)
	# loop over the detected barcodes
	out = []
	for barcode in barcodes:
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		# draw the barcode data and barcode type on the image
		text = "{}".format(barcodeData)
		#print(text)
		out.append(text)
	return out

	vs.stop()

num_qrs = 10

def exchange(username, canvas, max_msgs_power = 5):
	"""
	Desc: a func that transmits and reads qrcodes to transmit two parts of a one time pad. returns a tuple
			with the other's username, then the entire key;
	arg username: a string that represents the username to transmit;
	arg key: the key to transmit;
	arg canvas: a tkinter canvas that will be drawn on to display the bitmap;
	kwarg max_msgs_power: log base ten of the maximum number of msages that can be passed;
	"""

	first_header = "pos=0, username='"+usernames#_____ will be replaced

	std_header = 'pos='+'_'*max_msgs_power

	msgs = [first_header] #messages
	while len(msgs) < num_qrs:
		msgs.append(std_header)

	if len(msgs) > 10**max_msgs_power:
		return exchange(username, key, show_svg, msg_len = msg_len, max_msgs_power = max_msgs_power + 1)

	my_key = ''

	"""
	first_chunk_len = msg_len - first_header_len
	print(first_chunk_len)
	first_chunk = key[0:first_chunk_len]
	key = key[first_chunk_len:]

	first_msg = first_header + first_chunk
	msgs.append(first_msg)

	while len(key):
		msg = std_header + key[0:chunk_len]
		msgs.append(msg)
		key = key[chunk_len:]

	if len(msgs) > 10**max_msgs_power:
		return exchange(username, key, show_svg, msg_len = msg_len, max_msgs_power = max_msgs_power + 1)

	for index in range(len(msgs)):
		pos = str(index)
		while len(pos) < max_msgs_power:
			pos = '0'+pos

		msgs[index] = msgs[index].replace('_'*max_msgs_power, pos)

	print(msgs)
	print([len(msg) for msg in msgs])"""

exchange('JONAHYM', , 7, msg_len = 64)
