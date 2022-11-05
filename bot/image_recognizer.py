from io import BytesIO

from bot import constants

import cv2
import numpy as np
import pytesseract


def photo_2_text(image: BytesIO, language):
    """
    recognize text from image
    :param language: short name of language
    :param image: object BytesIO
    :return: recognized text
    """

    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(img, lang=language)
    if text == '':
        return constants.IMAGE_TEXT_UNRECOGNIZED

    return text
