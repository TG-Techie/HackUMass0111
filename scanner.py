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

num_qrs_pre_msg = 12

def scan_for_qrs():
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
		print(text)
		#print(text)
		out.append(text)
	return out

	vs.stop()


def exchange(username, canvas, max_msgs_power = 5, switching_time = 1):
	"""
	Desc: a func that transmits and reads qrcodes to transmit two parts of a one time pad. returns a tuple
			with the other's username, then the entire key (as a bytes object);
	arg username: a string that represents the username to transmit;
	arg key: the key to transmit;
	arg canvas: a tkinter canvas that will be drawn on to display the bitmap;
	kwarg max_msgs_power: log base ten of the maximum number of msages that can be passed;
	"""
	num_qrs = num_qrs_pre_msg

	qr_front = "[OptIn]"
	qr_end_front = '[OptInEND]'

	first_header = qr_front+"pos=0, username='"+username#_____ will be replaced

	std_header = qr_front+'pos='+'_'*max_msgs_power

	headers = [first_header] #messages
	while len(headers) < num_qrs:
		headers.append(std_header)

	#if len(headers) > 10**max_msgs_power:
	#	return exchange(username, canvas, max_msgs_power = max_msgs_power + 1, switching_time = switching_time)

	my_key = bytes()
	qrs = []
	for index, header in enumerate(headers):
		pos = str(index)
		#while len(pos) < max_msgs_power:
			#pos = '0'+pos

		qr_tup = bitmap.string_and_otp_bitmap(header.replace('_'*max_msgs_power, pos), '|', 64)
		my_key += qr_tup[0]

		qrs.append(qr_tup[1])

	#transmit and scan for qrs
	last_time_qr_switched = time.monotonic()

	transmition_complete_confirmed = False
	end_qr_posted = False
	found = []
	should_continue = True

	while should_continue:
		if (len(found) == num_qrs) and not end_qr_posted:
			bitmap.write_bitmap_to_canvas(bitmap.string_to_bitmap(qr_end_front)[1], canvas)
			end_qr_posted = True
		if transmition_complete_confirmed == False:
			if (time.monotonic() - last_time_qr_switched) > switching_time:

				bitmap.write_bitmap_to_canvas(qrs[0], canvas)

				qrs.append(qrs.pop(0))
				last_time_qr_switched = time.monotonic()

		if len(found) < num_qrs:
			#raw_found_qrs =
			for qr in scan_for_qrs():
				if qr.starswith(qr_front):
					if qr not in found:
						found.append(qr)
				elif qr.startswith(qr_end_front):
					transmition_complete_confirmed = True

		if transmition_complete_confirmed and end_qr_posted:
			break
			
	print(found)





exchange('JONAHYM', 'foe canvas here')
