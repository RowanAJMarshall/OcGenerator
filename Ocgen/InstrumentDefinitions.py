# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains instrument definitions and the Instrument superclass

import abc
import math

from PIL import Image


class Instrument(object, metaclass=abc.ABCMeta):
    X_CONST = None
    Y_CONST = None
    IMAGES_PER_SPRITE_SHEET_LINE = None
    IMAGES_PER_LINE_TABS = None
    NUM_OF_NOTES = None
    SPRITE_SHEET = None

    @abc.abstractmethod
    def get_notes(self):
        raise NotImplementedError("You must define get_notes to use this base class")

    def get_tabs_size(self, notes: list) -> tuple:
        x = self.IMAGES_PER_LINE_TABS * self.X_CONST
        y = math.ceil(len(notes) / self.IMAGES_PER_SPRITE_SHEET_LINE) * self.Y_CONST
        return x, y

    def get_note_box(self, x_val, y_val):
        return x_val, y_val, x_val + self.X_CONST, y_val + self.Y_CONST

    def construct_tabs(self, notes: list):
        size_tuple = self.get_tabs_size(notes)
        new_image = Image.new('RGB', size_tuple, color=(225, 241, 241))
        count = 0
        x_pos = 0
        y_pos = 0
        for note in notes:
            count += 1
            tab = self.get_image(note[2])
            new_image.paste(tab, self.get_note_box(x_pos, y_pos))
            x_pos += self.X_CONST
            if count == self.IMAGES_PER_LINE_TABS:
                y_pos += self.Y_CONST
                x_pos = 0
                count = 0
            if type("str") == str:
                pass
        return new_image

    # Retrieves the note image represented by num, extracted from a sprite sheet
    def get_image(self, num: int):
        if num > self.NUM_OF_NOTES or num < 0:
            raise ValueError("You entered {}: Number must be between 1 and {}".format(num, self.NUM_OF_NOTES))
        x_val = 0
        y_val = 0
        while num > self.IMAGES_PER_SPRITE_SHEET_LINE:
            y_val += self.Y_CONST
            num -= self.IMAGES_PER_SPRITE_SHEET_LINE

        for i in range(1, num):
            x_val += self.X_CONST

        img = Image.open(self.SPRITE_SHEET)
        box = self.get_note_box(x_val, y_val)
        return img.crop(box)


class TwelveHoleOcarina(Instrument):
    X_CONST = 129
    Y_CONST = 119
    IMAGES_PER_SPRITE_SHEET_LINE = 11
    IMAGES_PER_LINE_TABS = 10
    NUM_OF_NOTES = 21
    SPRITE_SHEET = 'images/12_hole.png'

    def __init__(self):
        pass

    def get_notes(self):
        return [["A", 440, 1], ["A\#", 466.16, 2], ["B", 493.88, 3], ["C", 523.25, 4], ["C\#", 554.37, 5],
                ["D", 587.33, 6],
                ["D\#", 622.25, 7], ["E", 659.26, 8], ["F", 698.46, 9], ["F\#", 739.99, 10], ["G", 783.99, 11],
                ["G#", 830.61, 12], ["A", 880, 13], ["A\#", 932.33, 14], ["B", 987.77, 15], ["C", 1046.5, 16],
                ["C\#", 1108.73, 17], ["D", 1174.66, 18], ["D\#", 1244.51, 19], ["E", 1318.51, 20], ["F", 1396.91, 21]]


class SixHoleOcarina(Instrument):
    X_CONST = 122
    Y_CONST = 84
    IMAGES_PER_SPRITE_SHEET_LINE = 1
    IMAGES_PER_LINE_TABS = 10
    NUM_OF_NOTES = 10
    SPRITE_SHEET = 'images/6_hole.png'

    def __init__(self):
        pass

    def get_notes(self):
        return [["C", 523.25, 1],
                ["D", 587.33, 2],
                ["E", 659.26, 3],
                ["F", 698.46, 4],
                ["G", 783.99, 5],
                ["A", 880, 6],
                ["B", 987.77, 7],
                ["C", 1046.5, 8],
                ["D", 1174.66, 9],
                ["E", 1318.51, 10]]
