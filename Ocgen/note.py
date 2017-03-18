class Note:
    def __init__(self, pitch: int, pitch_num: int):
        self.pitch = pitch
        self.pitch_num = pitch_num

# [(Note, Frequency, Integer representation)]
notes = [("A", 440, 1), ("A\#", 466.16, 2), ("B", 493.88, 3), ("C", 523.25, 4), ("C\#", 554.37, 5), ("D", 587.33, 6),
         ("D\#", 622.25, 7), ("E", 659.26, 8), ("F", 698.46, 9), ("F\#", 739.99, 10), ("G", 783.99, 11),
         ("G#", 830.61, 12), ("A", 880, 13), ("A\#", 932.33, 14), ("B", 987.77, 15), ("C", 1046.5, 16),
         ("C\#", 1108.73, 17), ("D", 1174.66, 18), ("D\#", 1244.51, 19), ("E", 1318.51, 20), ("F", 1396.91, 21)]

times_shifted = 0


def find_closest_note(note):
    return min(notes, key=lambda x: abs(float(x[1]) - note))



