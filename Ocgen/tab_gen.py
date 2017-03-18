# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains code to construct tabs out of a given set of pitches

from PIL import Image
import sys
import math

from Ocgen import note

X_CONST = 129
Y_CONST = 119
IMAGES_PER_LINE = 10


# Returns the x and y pixel size of the generated tabs, based on number of notes
def get_tabs_size(notes: list) -> tuple:
    x = 10 * X_CONST
    y = math.ceil(len(notes)/IMAGES_PER_LINE) * Y_CONST
    return x, y


def construct_tabs(notes: list):
    size_tuple = get_tabs_size(notes)
    new_image = Image.new('RGB', size_tuple, color=(225,241,241))
    count = 0
    x_pos = 0
    y_pos = 0
    for note in notes:
        count += 1
        tab = get_image_12_hole(note[2])
        new_image.paste(tab, get_note_box(x_pos, y_pos))
        print(str(count))
        x_pos += X_CONST
        if count == 10:
            y_pos += Y_CONST
            x_pos = 0
            count = 0
        if type("str") == str:
            pass
    return new_image


def construct_notes(pitch_list):
    freq_list = []
    for pitch in pitch_list:
        freq_list.append(note.find_closest_note(pitch))
    return freq_list


def get_max_min_notes(notes: list):
    max = 0
    min = sys.maxsize
    for note in notes:
        if note.pitch < min:
            min = note.pitch
        elif note.pitch > max:
            max = note.pitch
    return max, min


def pitch_to_note_transform(pitches):
    min_note = sys.maxsize
    max_note = 0

    for pitch in pitches:
        if pitch < min_note:
            min_note = pitch
        elif pitch > max_note:
            max_note = pitch
    

# Returns a square image extracted fom a sprite sheet of ocarina notes
def get_note_box(x_val, y_val):
    return x_val, y_val, x_val + X_CONST, y_val + Y_CONST
    

# Retrieves the note image represented by num, extracted from a sprite sheet
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


