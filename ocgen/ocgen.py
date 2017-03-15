# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your goto tool for ocarina tablature generation!
#

import sys
import os
import aubio
import ocgen.tab_gen
from ocgen import tab_gen
import pydub


def extract_onsets(pitches, onset, source, hop_s=512//2):
    frames = 0
    onsets = []
    while True:
        samples, read = source()
        if onset(samples):
            print("%f" % onset.get_last_s())
            onsets.append(onset.get_last())
        frames += read
        if read < hop_s: break



def filter_pitches(downsample, pitches):
    return pitches[::downsample]


def in_bounds(avg_val, num):
    bounds = 25
    if num > avg_val + bounds or num < avg_val - bounds:
        return False
    return True


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
    

def get_pitches(filename: str) -> list:
    downsample = 1
    samplerate = 44100//downsample

    win_s = 4096//downsample
    hop_s = 512//downsample

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("freq")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []
    total_frames = 0
    
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        #print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break
    time = total_frames / float(samplerate)
    return pitches, time


def write_file(lst):
    with open("log.txt", 'w') as log:
        for l in lst:
            log.write("\n" + str(l))


def write_result(image):
    image.save("static/result.png")
    pass


def check_format(filepath):
    if filepath[len(filepath) - 3:] == "wav":
        return "wav"
    if filepath[len(filepath) - 3:] == "mp3":
        return "mp3"
    return ""


def standardise_format(filepath: str):
    if check_format(filepath) == "mp3":
        wav_filename = filepath.replace(".mp3", ".wav")
        pydub.AudioSegment.from_file(filepath).export(wav_filename, format='wav')




# Main entry point to program
def main(filepath: str, start_time=0, end_time=-1):
    standardise_format(filepath)
    pitch_list, time = get_pitches(filepath)
    lst = smooth_pitches(pitch_list, time)
    for l in lst:
        print(str(l))
    lst = tab_gen.construct_notes(lst)
    img = tab_gen.construct_tabs(lst)
    write_result(img)
    print("Finished")
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please give a filename")
        exit(0)
    

