# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains code/functions to extract pitches and notes from a music file

import sys

import aubio
import pydub

import InstrumentDefinitions
from Ocgen import note
from Ocgen import tab_gen
from Utils import config


# Checks if a value is within a set bound
from InstrumentDefinitions import TwelveHoleOcarina


def in_bounds(avg_val: int, num: int) -> bool:
    bounds = config.conf['bounds']
    if num > avg_val + bounds or num < avg_val - bounds:
        return False
    return True


# Collects pitches together and extract distinct notes
# Kind of a roll-your-own onset detection
def smooth_pitches(pitches: list) -> list:
    naive_notes = []
    avg_val = None
    min_count = config.conf['min_count']
    count = 0

    for num in pitches:
        num = int(num)
        if num < 50:
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
    times = []
    total_frames = 0
    # Loop over and store all pitches
    while True:
        time_s = total_frames / float(samplerate)
        samples, read = s()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read

        if time_s < start:
            continue
        elif time_s > end:
            break

        if read < hop_s: break
        print("%f %f %f" % (time_s, pitch, confidence))
        pitches += [pitch]
        times += [time_s]

    print(len(pitches))
    return pitches, times


# Write result to set location
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


# Uses Aubio to extract notes
def get_notes(filename):
    downsample = 1
    samplerate = 44100 // downsample
    if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

    win_s = 512 // downsample # fft size
    hop_s = 256 // downsample # hop size

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    notes_o = aubio.notes("default", win_s, hop_s, samplerate)
    note_list = []

    print("%8s" % "time","[ start","vel","last ]")

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        new_note = notes_o(samples)
        if (new_note[0] != 0):
            note_str = ' '.join(["%.2f" % i for i in new_note])
            note_list.append(new_note[0])
            print("%.6f" % (total_frames/float(samplerate)), new_note)
        total_frames += read
        if read < hop_s: break
    return note_list


# Main entry point to program
def main(filepath: str, start_time=0, end_time=-1):
    config.setup_main_config()
    filepath = standardise_format(filepath)
    try:
        pitch_list, times = get_pitches(filepath)
    except RuntimeError:
        return False, "Something went wrong during transcription"
    lst = smooth_pitches(pitch_list)
    # lst = get_notes(filepath)
    # new_list = []
    # for i in lst:
    #     new_list.append(aubio.miditofreq(i))


    s = '12-hole'
    if s == '12-hole':
        instrument = InstrumentDefinitions.TwelveHoleOcarina()
    elif s == '6-hole':
        instrument == SixHoleOcarina()

    try:
        shift = note.get_shift(lst, 0, [i[1] for i in instrument.get_notes()])
    except note.NotEnoughRangeError:
        return False, "The chosen instrument does not have enough range"

    lst = tab_gen.construct_notes(lst, instrument.get_notes(), shift)
    img = tab_gen.construct_tabs(lst, instrument)
    # lst = tab_gen.construct_notes(lst, note.get_12_hole_notes(), shift)
    # img = tab_gen.construct_tabs(lst)
    img.show()
    write_result(img)
    # Hello World!
    return True


# Ensure arguments are passed when called as command-line app
if __name__ == "__main__":
    if len(sys.argv) > 1:

        main(sys.argv[1])
    else:
        print("Please give a filename")
        exit(0)
    

