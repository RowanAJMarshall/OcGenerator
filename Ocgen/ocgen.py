# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains code/functions to extract pitches and notes from a music file

import sys
import os
import aubio
from Ocgen import tab_gen
import pydub
#import tab_gen


# Checks if a value is within a set bound
def in_bounds(avg_val: int, num: int) -> bool:
    bounds = 25
    if num > avg_val + bounds or num < avg_val - bounds:
        return False
    return True


# Collects pitches together and extract distinct notes
# Kind of a roll-your-own onset detection
def smooth_pitches(pitches: list, time: int) -> list:
    naive_notes = []
    avg_val = None
    min_count = 20
    count = 0

    for num in pitches:
        num = int(num)
        if num < 1:
            continue
        if avg_val is None:
            avg_val = num
        if in_bounds(avg_val, num):
            avg_val = int((num + avg_val)/2)
            count += 1
        else:
            if count < min_count:
                avg_val = None
                count = 0
                continue
            naive_notes.append(avg_val)
            avg_val = int(num)
            count = 1
    if count >= min_count:
        naive_notes.append(avg_val)
    return naive_notes
    

# Extract pitches from a given music file
def get_pitches(filename: str, start=0, end=sys.maxsize) -> list:
    # Downsampling inactive at the moment
    downsample = 1
    samplerate = 44100//downsample

    win_s = 4096//downsample
    hop_s = 512//downsample

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8
    # Uses Yin pitch detection algorithm
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("freq")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []
    total_frames = 0
    # Loop over and store all pitches
    while True:
        samples, read = s()
        if read/float(samplerate) < start:
            continue
        elif read/float(samplerate) > end:
            break
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break
    time = total_frames / float(samplerate)
    return pitches, time


def write_result(image):
    image.save("static/result.png")


# Checks format of given file, return string representation of format
# Only checks file extension so far
def check_format(filepath: str) -> str:
    if filepath[len(filepath) - 3:] == "wav":
        return "wav"
    if filepath[len(filepath) - 3:] == "mp3":
        return "mp3"
    if filepath[len(filepath) - 3:] == "ogg":
        return "ogg"
    return ""


# Converts mp3 and ogg giles to wav if needed
# Returns new filepath, post-conversion
def standardise_format(filepath: str) -> str:
    if check_format(filepath) == "mp3":
        wav_filename = filepath.replace(".mp3", ".wav")
        pydub.AudioSegment.from_file(filepath).export(wav_filename, format='wav')
        return wav_filename
    elif check_format(filepath) == "ogg":
        wav_filename = filepath.replace(".mp3", ".wav")
        pydub.AudioSegment.from_file(filepath).export(wav_filename, format='wav')
        return wav_filename
    return filepath


# Main entry point to program
def main(filepath: str, start_time=0, end_time=-1):
    filepath = standardise_format(filepath)
    pitch_list, time = get_pitches(filepath)
    lst = smooth_pitches(pitch_list, time)
    for l in lst:
        print(str(l))
    lst = tab_gen.construct_notes(lst)
    img = tab_gen.construct_tabs(lst)
    write_result(img)


# Ensure arguments are passed when called as command-line app
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please give a filename")
        exit(0)
    

