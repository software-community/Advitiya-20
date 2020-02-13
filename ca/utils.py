from PIL import Image
from PIL import ImageDraw

def get_ca_certifiate(name, college):
    img = Image.open("ca/templates/ca/Template.jpg")
    draw = ImageDraw.Draw(img)

    draw.text((10,10), name)
    draw.text((10,20), college)
    
    return img