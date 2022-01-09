import cv2
import socket
import struct
import math
import pdb

class FrameSegment(object):
    """ 
    Object to break down image frame segment
    if the size of image exceed maximum datagram size 
    """
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 256 # extract 64 bytes in case UDP frame overflown
    def __init__(self, sock, port, addr="127.0.0.1"):
        self.s = sock
        self.port = port
        self.addr = addr

    def udp_frame(self, img):
        """ 
        Compress image and Break down
        into data segments 
        """
        compress_img = cv2.imencode('.jpg', img)[1] # Encoding the image to an array
        dat = compress_img.tobytes()
        size = len(dat) 
        count = math.ceil(size/(self.MAX_IMAGE_DGRAM)) # Number of segments required to transport this fram
        array_start_pos = 0
        while count:
            array_end_pos = min(size, array_start_pos + self.MAX_IMAGE_DGRAM)
            self.s.sendto(struct.pack('b', count) + dat[array_start_pos:array_end_pos], (self.addr, self.port))
            array_start_pos = array_end_pos
            count -= 1


def main():
    """ Top level main function """
    # Set up UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 42069

    fs = FrameSegment(s, port)

    cap = cv2.VideoCapture(1)
    while (cap.isOpened()):
        _, frame = cap.read()
        fs.udp_frame(frame)
    cap.release()
    cv2.destroyAllWindows()
    s.close()

if __name__ == "__main__":
    main()