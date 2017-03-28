# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
#
import copy


class Note:
    def __init__(self, pitch: int, pitch_num: int):
        self.pitch = pitch
        self.pitch_num = pitch_num


# Throw in the current instrument is out of range
class NotEnoughRangeError(Exception):
    pass


# Representation of the range of a 12-hole ocarina or arbitrary tuning
def get_12_hole_notes():
    # [(Note, Frequency, Integer representation)]
    return [["A", 440, 1], ["A\#", 466.16, 2], ["B", 493.88, 3], ["C", 523.25, 4], ["C\#", 554.37, 5], ["D", 587.33, 6],
           ["D\#", 622.25, 7], ["E", 659.26, 8], ["F", 698.46, 9], ["F\#", 739.99, 10], ["G", 783.99, 11],
           ["G#", 830.61, 12], ["A", 880, 13], ["A\#", 932.33, 14], ["B", 987.77, 15], ["C", 1046.5, 16],
           ["C\#", 1108.73, 17], ["D", 1174.66, 18], ["D\#", 1244.51, 19], ["E", 1318.51, 20], ["F", 1396.91, 21]]


# Gets the octave shift required, if any
def get_shift(pitches: list, shift_num=0, ref_list=[i[1] for i in get_12_hole_notes()]):
    # Lowest current frequency
    lowest = min(shift(ref_list))

    # Highest current frequency
    highest = max(shift(ref_list))

    minimum_freq = min(pitches)
    maximum_freq = max(pitches)

    too_low = minimum_freq < lowest
    too_high = maximum_freq > highest

    # If the pitches cannot be represented with the current instrument setting
    if (too_low and too_high) or (shift_num < 0 and too_high) or (shift_num > 0 and too_low):
        raise NotEnoughRangeError
    # There are 1 or more pitches lower than the current octave setting
    elif too_low:
        return get_shift(pitches, shift_num - 1, shift(ref_list, -1))
    # There are 1 or more pitches higher than the current octave setting
    elif too_high:
        return get_shift(pitches, shift_num + 1, shift(ref_list, 1))
    return shift_num


# Shift the given list by shift_num ocataves
def shift(lst, shift_num=0):
    if shift_num < 0:
        return downshift(lst, shift_num)
    if shift_num > 0:
        return upshift(lst, shift_num)
    return lst


def find_closest_note(note: float, ref_notes, shift_amount=0):
    ref_notes = shift(ref_notes, shift_amount)
    return min(ref_notes, key=lambda x: abs(float(x[1]) - note))


def alt_find_closest_note1(note: float, ref_notes, shift_amount=0):

    ref_notes = shift(ref_notes, shift_amount)

    prev = ref_notes[0]
    for index, n in enumerate(ref_notes):
        if note == n[1]:
            return n
        elif note > n[1]:
            prev = n
            continue
        elif note < n[1]:
            return n
    return prev


# Ocatave-shift pitches up
def upshift(note_list: list, shift_num):
    note_list = copy.deepcopy(note_list)
    upshift_factor = 2 ** shift_num
    if type(note_list[0]) == list:
        for index, n in enumerate(note_list):
            note_list[index][1] *= upshift_factor
    else:
        for index, n in enumerate(note_list):
            note_list[index] *= upshift_factor
    return note_list

    # note_list = list(note_list)
    # upshift_factor = 2 ** shift_num
    # for index, n in enumerate(note_list):
    #     note_list[index][1] *= upshift_factor
    # return note_list


# Ocatave-shift pitches down
def downshift(note_list: list, shift_num):
    note_list = copy.deepcopy(note_list)
    downshift_factor = 2 ** abs(shift_num)
    if type(note_list[0]) == list:
        for index, n in enumerate(note_list):
            note_list[index][1] /= downshift_factor
    else:
        for index, n in enumerate(note_list):
            note_list[index] /= downshift_factor
    return note_list

    # note_list = list(note_list)
    # downshift_factor = 2 ** abs(shift_num)
    # for index, n in enumerate(note_list):
    #     note_list[index][1] /= downshift_factor
    # return note_list



# all_notes = [i for i in range(0, 128)]
# notes_12_hole = [(index+1, k) for index, k in enumerate(range(69, 91))]




