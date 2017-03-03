from PIL import Image
from note import Note
import sys

def get_max_min(notes: list):
    max = 0
    min =  sys.maxint
    for note in notes:
        if note.pitch < min:
            min = note.pitch
        elif note.pitch > max:
            max = note.pitch
    return max, min

def create_tabs(notes: list):
    max, min = get_max_min(notes)
    


def get_image_12_hole(num: int):
    if num > 21 or num < 0:
        raise ValueError("Number must be between 0 and 20")
    y_const = 119
    x_const = 129
    x_val = 0
    if num > 11:
        y_val = 119
        num -= 11
    else:
        y_val = 0

    for i in range(0, num):
        x_val += x_const

    img = Image.open("images/ocarinanotes.png")
    box = (x_val, y_val, x_val+x_const, y_val+y_const)
    return img.crop(box)


