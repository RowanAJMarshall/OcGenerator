# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your goto tool for ocarina tablature generation!
#

import sys
import os
import aubio
from ocgen.note import Note

def filter_pitches(downsample, pitches):
    return pitches[::downsample]

def in_bounds(avg_val, num):
    bounds = 2
    if num > avg_val + bounds or num < avg_val - bounds:
        return False
    return True


# Smooths out pitches, grouping them as an average within a set bound
def smooth_pitches(pitches: list, time: int) -> list:
    naive_notes = []
    avg_val = None
    min_count = 5
    count = 0
    for num in pitches:
        if avg_val == None:
            avg_val = num
        if in_bounds(avg_val, num):
            avg_val = int((num + avg_val)/2)
            count += 1
        else:
           # if count < min_count:
           #     avg_val = None
           #     count = 0
           #     continue
            naive_notes.append(Note(avg_val, count))
            avg_val = num
            count = 1
    naive_notes.append(Note(avg_val, count))
    return naive_notes
    

def get_pitches(filename: str) -> list:
    downsample = 1
    samplerate = int(44100/downsample)

    win_s = int(4096/downsample)
    hop_s = int(4096/downsample)

    #print(str(samplerate))
    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []
    total_frames = 0
    
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    print(len(pitches))






# Main entry point to program
def main(filepath: str):
    print(filepath)
    print(os.getcwd())
    pitch_list = get_pitches(filepath)
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please give a filename")
        exit(0)
    

