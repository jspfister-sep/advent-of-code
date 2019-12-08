import math, sys

BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'
WIDTH = 25
HEIGHT = 6

def get_pixel(front_pixel, back_pixel):
    if front_pixel == TRANSPARENT:
        return back_pixel
    return front_pixel

layer_size = WIDTH * HEIGHT
image = TRANSPARENT * layer_size

with open('data.txt', 'r') as f:
    while True:
        layer_data = f.read(layer_size)
        if len(layer_data) < layer_size:
            break
        image = ''.join(map(get_pixel, image, layer_data))

image = image.replace('0', ' ')
image = image.replace('1', '*')

for i in range(HEIGHT):
    print(image[i * WIDTH:(i + 1) * WIDTH])

