from PIL import Image, ImageDraw
import requests
from io import BytesIO

def write_on_image_with_coords_dict(image_url, coord_dict):
    img_data = requests.get(image_url).content
    img_bytesio_obj = BytesIO(img_data)
    pil_img = Image.open(img_bytesio_obj)
    for coord in coord_dict:
        ImageDraw.Draw(pil_img).text(coord, coord_dict[coord], (0, 0, 0))
    img_bytesio = BytesIO()
    pil_img.save(img_bytesio, "JPEG")
    img_bytesio.seek(0)
    return img_bytesio