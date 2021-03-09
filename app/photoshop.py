from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

def write_on_image_with_coords_dict(image_url, coord_dict):
    img_data = requests.get(image_url).content
    img_bytesio_obj = BytesIO(img_data)
    pil_img = Image.open(img_bytesio_obj)
    #font = ImageFont.truetype("app/fonts/arial.ttf", size = 40)
    img = ImageDraw.Draw(pil_img)
    for coord in coord_dict:
        text, font_size = coord_dict[coord]
        font = ImageFont.truetype("app/fonts/arial.ttf", size=font_size)
        img.text(coord, text, font = font, fill = (0, 0, 0))
    img_bytesio = BytesIO()
    pil_img.save(img_bytesio, "JPEG")
    img_bytesio.seek(0)
    return img_bytesio