import cv2
import imutils
from imutils.video import VideoStream
import time
import re

from pyzbar import pyzbar

import QR


class PathOptim:
    """
    Unit Tests for QR.py
    ...

    Attributes
    ----------
    scanner : QRScanner
        QR.py module
    videoStream : imutils.video.VideoStream
        Incoming video to be read

    Methods
    -------
    __init__()
        Initializes module, runs single image test & video test
    run_single_image_test(imagePath : str)
        Runs QR Scanner on a single, static image
    run_video_test()
        Runs QR Scanner on live video feed
    """

    def __init__(self):
        """
        Initializes module, runs single image test & video test
        """

        self.thisdict = {
            "Alpha": (48.5166707, -71.6375025),
            "Bravo": (48.506094, -71.63175187),
            "Charlie": (48.4921159, -71.6340069),
            "Delta": (48.5150341, -71.6404442),
            "Echo": (48.5005337, -71.6782955),
            "Foxtrot": (48.5088395, -71.6040591),
            "Golf": (48.5101473, -71.6522101),
            "Hotel": (48.5129917, -71.6426006),
            "India": (48.5117408, -71.6428152),
            "Juliette": (48.5193311, -71.6229056),
            "Kilo": (48.4984623, -71.6568088),
            "Lima": (48.5019885, -71.6253089),
            "Mike": (48.520525, -71.6720008),
            "November": (48.5090567, -71.6461702),
            "Oscar": (48.5107057, -71.6516848),
            "Papa": (48.5039667, 71.6298198),
            "Quebec": (48.5262308, -71.6345802),
            "Point": (48.511563, -71.6804996),
            "Romeo": (48.4984266, -71.6425625),
            "Sierra": (48.5258329, -71.6320911),
            "Tango": (48.4996779, -71.6758648),
            "Uniform": (48.4937058, -71.6290012),
            "Victor": (48.510353, -71.6228085),
            "Whiskey": (48.5093153, -71.6216069),
            "Xray": (48.4969248, -71.6034018),
            "Yankee": (48.5112557, -71.6312968),
            "Zulu": (48.4932846, -71.6664874)
        }

        self.scanner = QR.QRScanner()

        # imagePath = "task1QR1.png"
        # self.run_single_image_test(imagePath)

        self.videoStream = VideoStream(src=0).start()
        self.run_video_test()

    def run_single_image_test(self, imagePath):
        """
        Runs QR Scanner on a single, static image

        Parameters
        ----------
        imagePath : str
            Relative path to the image to be tested
        """
        image = cv2.imread(imagePath)
        image, output = self.scanner.main(image)

    def run_video_test(self):
        """
        Runs QR Scanner on live video feed
        """
        output = None

        while True:
            frame = self.videoStream.read()
            frame = imutils.resize(frame)

            frame, output = self.scanner.main(frame)
            cv2.imshow('video', frame)
            key = cv2.waitKey(1) & 0xFF
            if output or key == ord('q'):
                cv2.destroyAllWindows()
                break

        ispath = True
        if re.search("Avoid", output):
            output = output.replace("Avoid the area bounded by: ", "")
            output = output.replace(".  Rejoin the route at", ";")
            ispath = False
        else:
            output = output.replace("Follow route: ", "")


        output_list = (ispath, [(element, self.thisdict[element]) for element in output.split("; ")])
        print(output_list)

        self.videoStream.stop()


if __name__ == "__main__":
    PathOptim()