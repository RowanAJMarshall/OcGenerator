# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains code to construct tabs out of a given set of pitches

from PIL import Image
import sys
import math

import InstrumentDefinitions
from Ocgen import note

# X_CONST_12 = 129
# Y_CONST_12 = 119
# IMAGES_PER_LINE_12 = 11

X_CONST_6 = 106
Y_CONST_6 = 137
IMAGES_PER_LINE_6 = 16


# Returns the x and y pixel size of the generated tabs, based on number of notes
# def get_tabs_size(notes: list) -> tuple:
#     x = 10 * X_CONST_12
#     y = math.ceil(len(notes) / IMAGES_PER_LINE_12) * Y_CONST_12
#     return x, y


# Given a list of frequencies, constructs a new tab image
def construct_tabs(notes: list, instrument: InstrumentDefinitions.Instrument):
    return instrument.construct_tabs(notes)


# Constructs a note list based on the closest frequencies
def construct_notes(pitch_list, ref_notes, shift_amount=0):
    freq_list = []
    for pitch in pitch_list:
        freq_list.append(note.find_closest_note(pitch, ref_notes, shift_amount))
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
# def get_note_box_12_hole(x_val, y_val):
#     return x_val, y_val, x_val + X_CONST_12, y_val + Y_CONST_12
#
#
# def get_note_box_6_hole(x_val, y_val):
#     return x_val, y_val, x_val + X_CONST_6, y_val + Y_CONST_6



    




