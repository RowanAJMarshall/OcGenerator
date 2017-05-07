# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains code to construct tabs out of a given set of pitches

import sys

from Ocgen import InstrumentDefinitions
from Ocgen import note


X_CONST_6 = 106
Y_CONST_6 = 137
IMAGES_PER_LINE_6 = 16


# Given a list of frequencies, constructs a new tab image
def construct_tabs(notes: list, instrument: InstrumentDefinitions.Instrument):
    return instrument.construct_tabs(notes)


# Constructs a note list based on the closest frequencies
def construct_notes(pitch_list, ref_notes, shift_amount=0):
    freq_list = []
    for pitch in pitch_list:
        freq_list.append(note.find_closest_note(pitch, ref_notes, shift_amount))
    return freq_list


def pitch_to_note_transform(pitches):
    min_note = sys.maxsize
    max_note = 0

    for pitch in pitches:
        if pitch < min_note:
            min_note = pitch
        elif pitch > max_note:
            max_note = pitch
