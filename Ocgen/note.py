# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
#


class Note:
    def __init__(self, pitch: int, pitch_num: int):
        self.pitch = pitch
        self.pitch_num = pitch_num


def get_12_hole_notes():
    # [(Note, Frequency, Integer representation)]
    return [["A", 440, 1], ["A\#", 466.16, 2], ["B", 493.88, 3], ["C", 523.25, 4], ["C\#", 554.37, 5], ["D", 587.33, 6],
           ["D\#", 622.25, 7], ["E", 659.26, 8], ["F", 698.46, 9], ["F\#", 739.99, 10], ["G", 783.99, 11],
           ["G#", 830.61, 12], ["A", 880, 13], ["A\#", 932.33, 14], ["B", 987.77, 15], ["C", 1046.5, 16],
           ["C\#", 1108.73, 17], ["D", 1174.66, 18], ["D\#", 1244.51, 19], ["E", 1318.51, 20], ["F", 1396.91, 21]]


def find_closest_note1(note):
    return min(get_12_hole_notes(), key=lambda x: abs(float(x[1]) - note))


def find_closest_note(note, shift=0):
    notes = get_12_hole_notes()
    if shift > 0: notes = upshift(notes, shift)
    elif shift < 0: notes = downshift(notes, shift)

    prev = notes[0]
    for index, n in enumerate(notes):
        if note == n[1]:
            return n
        elif note > n[1]:
            prev = n
            continue
        elif note < n[1]:
            return prev
    return prev


def upshift(note_list: list, shift):
    upshift_factor = 2 ** shift
    for index, n in enumerate(note_list):
        note_list[index][1] *= upshift_factor
    return note_list


def downshift(note_list: list, shift):
    downshift_factor = 2 ** abs(shift)
    for index, n in enumerate(note_list):
        note_list[index][1] /= downshift_factor
    return note_list



# all_notes = [i for i in range(0, 128)]
# notes_12_hole = [(index+1, k) for index, k in enumerate(range(69, 91))]




