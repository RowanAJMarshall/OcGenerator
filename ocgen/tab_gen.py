from PIL import Image
from ocgen.note import Note
import sys
import math

X_CONST = 129
Y_CONST = 119
IMAGES_PER_LINE = 10

def get_tabs_size(notes: list):
    x = 10 * X_CONST #len(notes) * X_CONST
    y = math.ceil(len(notes)/IMAGES_PER_LINE) * Y_CONST
    return x, y


def construct_tabs(notes: list):
    size_tuple = get_tabs_size(notes)
    new_image = Image.new('RGB', size_tuple)
    count = 0
    x_pos = 0
    y_pos = 0
    for note in notes:
        count += 1
        # colour = e1f1f1
        tab = get_image_12_hole(note)
        new_image.paste(tab, get_note_box(x_pos, y_pos))
        print(str(count))
        x_pos += X_CONST
        if count == 10:
            y_pos += Y_CONST
            x_pos = 0
            count = 0
    return new_image


def overlay_notes(notes: list):
    pass

def get_max_min_notes(notes: list):
    max = 0
    min = sys.maxsize
    for note in notes:
        if note.pitch < min:
            min = note.pitch
        elif note.pitch > max:
            max = note.pitch
    return max, min


def create_tabs(notes: list):
    max, min = get_max_min_notes(notes)
    overlay = overlay_notes(notes)


def get_note_box(x_val, y_val):
    return x_val, y_val, x_val + X_CONST, y_val + Y_CONST
    

def get_image_12_hole(num: int):
    if num > 21 or num < 0:
        raise ValueError("Number must be between 0 and 20")
    x_val = 0
    if num > 11:
        y_val = 119
        num -= 11
    else:
        y_val = 0

    for i in range(1, num):
        x_val += X_CONST

    img = Image.open("images/ocarinanotes.png")
    box = get_note_box(x_val, y_val)
    return img.crop(box)


