from PIL import Image
from PIL import ImageDraw, ImageFont

def get_ca_certifiate(name, college):
    img = Image.open("ca/templates/ca/Marketing_Intern.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("ca/templates/ca/SansSerif.ttf", 72)

    draw.text((600,1235), name, (0, 0, 0), font=font, stroke_width=1)
    draw.text((250,1385), college, (0, 0, 0), font=font, stroke_width=1)
    
    return img