from PIL import Image
import os
#currDir = os.getcwd()
x = 50
os.chdir(os.getcwd() + '\\Title Screen')
for file in os.listdir(os.getcwd()):
    img = Image.open(file)
    img = img.resize((720, 520))
    img.save(file)
