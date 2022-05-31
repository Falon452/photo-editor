import cv2
from PIL import Image
import numpy as np


class ComputionalPhotography:
    def __init__(self, parent):
        self.parent = parent

    def denoise(self, img):
        img = np.array(img)
        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        res = Image.fromarray(img)
        return res

    def inpaint(self, img):
        return NotImplementedError
        return cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    def hdr(self, img):
        return img
