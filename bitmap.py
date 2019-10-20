from nayuki_qrcodegen.qrcodegen import *
import os

def binary_to_bitmap(data, write_svg=False):
    """
    Returns a QR Code bitmap for the binary data with the following properties:
     - Pixels are referenced by bitmap[y][x] with top left corner (x=0, y=0)
     - Pixel values are False = white, True = black
    """
    qr_code = QrCode.encode_binary(data, QrCode.Ecc.LOW)

    if write_svg:
        qr_code_svg = open('qr-code.svg', 'w')
        qr_code_svg.write(qr_code.to_svg_str(1))
        qr_code_svg.close()
    
    return qr_code._modules

def string_to_bitmap(string, write_svg=False):
    """
    Returns a QR Code bitmap for the ASCII string with the following properties:
     - Pixels are referenced by bitmap[y][x] with top left corner (x=0, y=0)
     - Pixel values are False = white, True = black
    """
    return binary_to_bitmap(string.encode('ascii'), write_svg)

def bitmap_to_repr(bitmap, black='[]', white='  ', eol='\n'):
    """
    Returns a string representation of a QR Code bitmap.
    """
    string = ''
    for col in bitmap:
        for val in col:
            if val:
                string += black
            else:
                string += white
        string += eol
    return string

def otp_bitmap(size=2953, write_svg=False):
    """
    Returns a tuple including a cryptographically secure one time pad byte array
    and its QR Code bitmap.
    """
    otp = os.urandom(size)
    return (otp, binary_to_bitmap(otp, write_svg))

def string_and_otp_bitmap(string, sepchar, size, write_svg=False):
    """
    Returns a tuple including a byte array containing first a string, separating character,
    and a cryptographically secure one time pad and second its QR Code bitmap.
    """
    otp = os.urandom(size)
    return (otp, binary_to_bitmap(bytearray().join([(string + sepchar).encode('ascii'), otp]), write_svg))

def write_bitmap_to_canvas(bitmap, w):
    """
    Writes a bitmap to a Tkinter canvas for scanning purposes
    """
    bitmap_size = len(bitmap)
    w_width = w.info_width()
    w_height = w.info_height()
    
    canvas.create_rectangle(0, 0, w_width, w_height, fill="white", outline="")
    
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
                canvas.create_rectangle(x * rect_size + x_offset, y * rect_size + y_offset, 
                                            (x + 1) * rect_size + x_offset, (y + 1) * rect_size + y_offset, 
                                            fill="black", outline="")
            else:
                canvas.create_rectangle(x * rect_size + x_offset, y * rect_size + y_offset, 
                                            (x + 1) * rect_size + x_offset, (y + 1) * rect_size + y_offset, 
                                            fill="white", outline="")

