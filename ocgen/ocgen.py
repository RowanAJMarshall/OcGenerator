# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your goto tool for ocarina tablature generation!
#

import sys
import os
import aubio

def get_pitches(filename: str) -> list:
    downsample = 1
    samplerate = 44100//downsample

    win_s = 4096//downsample
    hop_s = 512//downsample

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

    if 0: sys.exit(0)

 #   for i, p in enumerate(pitches):
 #       print("Time: " + str(samples[i]) + ", Pitch: " + str(p))






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
    

