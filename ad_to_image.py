from PIL import Image
import os

MAX_SIZE = 1024
QUALITY = 80


class ADConverter(object):
    def __init__(self):
        # Create the images folder if it doesn't exist
        self.dir = "./images/"
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def convert_to_jpg(self, data):
        path = "%sout.jpg" % self.dir
        img = Image.frombuffer('L', (data[1], data[2]), data[0], 'raw', 'L', 0, 1)
        img.save(path, "JPEG", quality=QUALITY)
        if img.width > MAX_SIZE or img.height > MAX_SIZE:
            self._resize_image(path)
        return os.path.abspath(path)

    def _resize_image(self, path):
        # For some reason we have to save then reopen the file to be able to resize it correctly!
        img = Image.open(path)
        img.thumbnail((MAX_SIZE, MAX_SIZE), Image.NEAREST)
        img.save(path, "JPEG", quality=QUALITY)
