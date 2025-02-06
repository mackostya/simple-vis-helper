# "One does not simply ..." meme generator with 4K resolution
# TODO: remove the hardcoded values and make it dynamic
# TODO: rewrite it with PyQT into an inteactable sofware

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

img = Image.open("imgs/meme.png")
print(img.size)
img = img.crop((760, 0, img.size[0] - 630, img.size[1]))
draw = ImageDraw.Draw(img)

version = "v1"

font = ImageFont.truetype("impact.ttf", 270)
draw.text((80, 30), "ONE DOES NOT SIMPLY", (255, 255, 255), font=font)

draw.text((170, 1290), "WALK INTO MORDOR", (255, 255, 255), font=font)

img.save("meme-out.jpg")
