import easyocr
from typing import List
from PIL import Image, ImageOps
import numpy as np

class ImageReader:
    def __init__(self):
        pass

    def get_text_from_img(self, img_path: str) -> List:
        
        # Open the file
        reader = easyocr.Reader(['de'], gpu=True)
        pil_img =Image.open(img_path).convert('RGB')

        # Transpose the file (cause it may be rotated) and crop it to reduce any noise
        pil_img = ImageOps.exif_transpose(pil_img)
        left_column = pil_img.crop((0, 0, int(pil_img.width*2/5), pil_img.height))

        # Convert the image into a numpy array for EasyOCR and return the text list
        img_array = np.array(left_column)
        return reader.readtext(img_array, detail=0)