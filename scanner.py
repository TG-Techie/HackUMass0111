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
import tkinter as tk

num_qrs_pre_msg = 5

import threading

class QRFrame(tk.Frame):

    def __init__(self, controller, bitmap):
        super().__init__(controller)

        canv = tk.Canvas(self, width =512, height = 512)
        canv.pack()
        w = canv

        bitmap_size = len(bitmap)
        w_width = 512
        w_height = 512

        a = w.create_rectangle(0, 0, w_width, w_height, fill="WHITE", outline="")
        w.move(a, 20, 20)

        x_offset = 0
        y_offset = 0
        w_size = 0
        if w_width < w_height:
            w_size = w_width
            y_offset = (w_height - w_width) // 2
        else:
            w_size = w_height
            x_offset = (w_width - w_height) // 2
        rect_size = w_size // bitmap_size
        for y in range(bitmap_size):
            for x in range(bitmap_size):
                if bitmap[y][x]:
                    w.create_rectangle(x * rect_size + x_offset, y * rect_size + y_offset,
                                                (x + 1) * rect_size + x_offset, (y + 1) * rect_size + y_offset,
                                                fill="black", outline="")
                else:
                    w.create_rectangle(x * rect_size + x_offset, y * rect_size + y_offset,
                                                (x + 1) * rect_size + x_offset, (y + 1) * rect_size + y_offset,
                                                fill="white", outline="")

class qr_display(tk.Tk):

	def __init__(self):
		super().__init__()
		self.stay_alive = True
		self._frame = None

	def new_qr_frame(self, qr):
		if self.stay_alive != True:
			print('QUITING!!!!!!!')
			self.quit()

		nf = QRFrame(self, qr)
		if self._frame is not None:
		    self._frame.destroy()
		self._frame = nf
		self._frame.pack()




def scan_for_qrs():
	"""
	Desc: scans once for a qr code and returns a list of all the codes found;
	"""
	# construct the argument parser and parse the arguments
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	#	help="path to output CSV file containing barcodes")
	#args = vars(ap.parse_args())
	print('scanning')
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
	print('TG! scan_for_qr:', out)
	return out

	vs.stop()


def exchange(username, max_msgs_power = 5, switching_time = 1):
	"""
	Desc: a func that transmits and reads qrcodes to transmit two parts of a one time pad. returns a tuple
			with the other's username, then the entire key (as a bytearray);
	arg username: a string that represents the username to transmit;
	arg key: the key to transmit;
	arg canvas: a tkinter canvas that will be drawn on to display the bitmap;
	kwarg max_msgs_power: log base ten of the maximum number of msages that can be passed;
	"""
	num_qrs = num_qrs_pre_msg

	qr_front = "[OptIn]"
	qr_end_front = '[OptInEND]'

	first_header = qr_front+"[_____,'"+username+"']"#_____ will be replaced

	std_header = qr_front+'['+('_'*max_msgs_power)+']'

	headers = [first_header] #messages
	while len(headers) < num_qrs:
		headers.append(std_header)

	#if len(headers) > 10**max_msgs_power:
	#	return exchange(username, canvas, max_msgs_power = max_msgs_power + 1, switching_time = switching_time)

	my_key = bytearray()
	qrs = []
	for index, header in enumerate(headers):
		pos = str(index)
		#while len(pos) < max_msgs_power:
			#pos = '0'+pos

		qr_tup = bitmap.string_and_otp_bitmap(header.replace('_'*max_msgs_power, pos), '|', 48)
		#bytearray().join([my_key, qr_tup[0]])
		my_key.extend(qr_tup[0])

		qrs.append(qr_tup[1])

	#transmit and scan for qrs
	last_time_qr_switched = time.monotonic()

	transmition_complete_confirmed = False
	end_qr_posted = False
	found = []
	should_continue = True

	#my_key = my_key.decode("unicode")
	print('!!!!!!!!my_key', my_key)

	global output
	output = qr_display()
	def show_canvas(qr):
		global output
		#output.destroy()
		#output = qr_display()
		output.new_qr_frame(qr)
		output.update()


	#thread.daemon = True


	while should_continue:
		print(len(found))
		if (len(found) == num_qrs):
			#canvas = tk.Canvas(master, width = 512, height = 512)
			#bitmap.write_bitmap_to_canvas(bitmap.string_to_bitmap(qr_end_front), canvas)
			#show_canvas(canvas)
			show_canvas(bitmap.string_to_bitmap(qr_end_front))
			#show_new_qr(bitmap.string_to_bitmap(qr_end_front))
			end_qr_posted = True

		if (transmition_complete_confirmed == False) or  (len(found) < num_qrs) :
			if (time.monotonic() - last_time_qr_switched) > switching_time:

				print('puttin new qr on screen')
				show_canvas(qrs[0])

				qrs.append(qrs.pop(0))
				last_time_qr_switched = time.monotonic()

		#if not transmition_complete_confirmed:
			#raw_found_qrs =
			for qr in scan_for_qrs():
				print('in scn loop',qr)
				if qr.startswith(qr_front):
					if qr not in found:
						found.append(qr)
						print(qr)
				elif qr.startswith(qr_end_front):
					transmition_complete_confirmed = True


		if transmition_complete_confirmed and end_qr_posted and (len(found) == num_qrs):
			proced_qrs = [qr.replace(qr_front, '').split('|') for qr in found]
			print(proced_qrs)

			proced_qrs.sort(key = lambda item: eval(item[0])[0])

			other_username = eval(proced_qrs[0][0])[1]
			other_key = bytearray()
			for pqr in proced_qrs:
				#print(pqr[1], bytes(pqr[1].encode('ascii')))
				#other_key += bytearray().join([pqr[1]])
				print(pqr[1])
				other_key.extend(map(ord, pqr[1]))

			print(other_key)
			print(proced_qrs)
			#print(bytes(other_key) == bytes(my_key))

			master_key = bytearray()

			if hash(username) > hash(other_username):
				master_key.extend(my_key)
				master_key.extend(other_key)
			else:
				master_key.extend(other_key)
				master_key.extend(my_key)
			print('\n'*5)
			print('masterkey',master_key )
			output.destroy()
			break
	return (other_username, master_key)
#b'{\xd5\xe5\xe1\x97l!\x16/nB\xe0\x1db\x95\xf6A\x1f\xeb\x15\xa7HXcc\x96O\xd4\x06j~/\xb9\xe5\xc15\t\xba\xc6\x8f\xb4m\n5\x12Er9$\xe4H\x85\xf8-\x90\x05rV\x8d\x00\xfd\x03\xfd@\xebJ\xf8_\xa2L@\xbe\xfav\xf7+8aq\x92\xbe\x88\xae\xa5\xc5)\xb2/\xe0\x0c\xcb\x07\xad\xa6\x18t\x1c\xc79\xde={\xc3E[\x82\x03|\xe0\x9a\xd3`_\xcd\x1e1\x82u\x83;\x0bUw\xb2\xc1q\x992'

#exchange('joanh', tk.Tk(), print)
