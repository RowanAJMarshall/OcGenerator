# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your go-to tool for ocarina tablature generation!
#
# This file contains code/functions to extract pitches and notes from a music file
import sys
import os
import aubio

from AudioConversion import convert
from Ocgen import InstrumentDefinitions
from Ocgen import note
from Ocgen import tab_gen
from Utils import config
from Utils.file_utilities import seperate_path_and_file


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
def get_pitches(filename: str, start, end, pitch_algorithm) -> list:
    # Downsampling inactive at the moment
    downsample = 1
    samplerate = 44100//downsample
    win_s = 4096//downsample
    hop_s = 512//downsample
    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    tolerance = 0.8
    # Uses Yin pitch detection algorithm
    pitch_o = aubio.pitch(pitch_algorithm, win_s, hop_s, samplerate)
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
        # print("%f %f %f" % (time_s, pitch, confidence))
        pitches += [pitch]
        times += [time_s]

    return pitches, times


def write_result(image, name: str):
    _, new_filename = seperate_path_and_file(name)
    image.save("static/" + new_filename.replace(".wav",".png"))

    return new_filename.replace(".wav",".png")


# Checks format of given file, return string representation of format
# Only checks file extension so far
def check_format(filepath: str, char_num) -> str:
    if filepath[len(filepath) - char_num:] == "wav":
        return "wav"
    if filepath[len(filepath) - char_num:] == "mp3":
        return "mp3"
    if filepath[len(filepath) - char_num:] == "ogg":
        return "ogg"
    if filepath[len(filepath) - char_num:] == "webm":
        return "webm"
    return ""


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







class NoValidInstrumentException(Exception):
    pass


def get_instrument(instrument_name: str) -> InstrumentDefinitions.Instrument:
    if instrument_name == '12-hole':
        return InstrumentDefinitions.TwelveHoleOcarina()
    elif instrument_name == '6-hole':
        return InstrumentDefinitions.SixHoleOcarina()
    raise NoValidInstrumentException


# Main entry point to program
def main(filepath: str, start_time: int, end_time: int, instrument_name: str, pitch_algorithm: str, shifting: bool):
    config.setup_main_config()

    try:
        filepath = convert.standardise_format(filepath)
        pitch_list, times = get_pitches(filepath, start_time, end_time, pitch_algorithm)
    except RuntimeError:
        return "Something went wrong during transcription", None
    except convert.NotSupportedException:
        return "File format is not supported", None

    lst = smooth_pitches(pitch_list)
    instrument = get_instrument(instrument_name)
    not_enough_range_error = "The chosen instrument does not have enough range", None

    # Get the octave shift needed to accurately transcribe song
    try:
        shift = note.get_shift(lst, 0, [i[1] for i in instrument.get_notes()])
    except note.NotEnoughRangeError:
        return not_enough_range_error
    # If user doesn't want to use octave shifting, make sure no shifting is necessary. If it is, return error.
    if not shifting and shift != 0:
        return "The chosen instrument does not have enough range. Try turning on octave shifting.", None

    lst = tab_gen.construct_notes(lst, instrument.get_notes(), shift)
    img = tab_gen.construct_tabs(lst, instrument)

    img_name = write_result(img, filepath)

    return None, img_name


# Ensure arguments are passed when called as command-line app
if __name__ == "__main__":
    if len(sys.argv) > 1:

        main(sys.argv[1], 0, sys.maxsize, '12-hole', 'yin')
    else:
        print("Please give a filename")
        exit(0)
    

