"""
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
sudo apt-get install tesseract-ocr-[ukr]
sudo apt-get install tesseract-ocr-[rus]
"""
import cv2
import pytesseract


def photo_2_text(path_to_image, language):  # some oe sting comment
    """
    recognize text from image
    :param language: short name of language
    :param path_to_image: filename .jpg
    :return: recognized text
    """

    img = cv2.imread(path_to_image)
    text = pytesseract.image_to_string(img, lang=language)
    if text == '':
        return 'На жаль, мені не вдалося розпізнати текст на фото :('
    return text

# https://translate.yandex.com/ocr
"""
img = cv2.imread('/home/darkor/Pictures/Screenshot from 2020-02-02 14-05-17.png')
text = pytesseract.image_to_string(image=img, lang='ua')
print(text)
"""
