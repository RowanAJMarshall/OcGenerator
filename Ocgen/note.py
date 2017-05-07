# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
#
import copy


# Throw in the current instrument is out of range
class NotEnoughRangeError(Exception):
    pass


# Gets the octave shift required, if any
def get_shift(pitches: list, shift_num=0, ref_list=0):
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


# Finds the closest note to the given note value and returns it
def find_closest_note(note: float, ref_notes, shift_amount=0):
    ref_notes = shift(ref_notes, shift_amount)
    return min(ref_notes, key=lambda x: abs(float(x[1]) - note))


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




