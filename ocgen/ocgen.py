# Written by Rowan Marshall
# Licensed under the MIT License (https://opensource.org/licenses/MIT)
#
# OcGenerator - Your goto tool for ocarina tablature generation!
#

import sys
import os
import aubio

class MusicFile:
    def __init__(self, filename):
        self.filename = filename



# Main entry point to program
def main(filepath):
    print(filepath)
    print(os.getcwd())
    pitch_list = get_pitches()
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please give a filename")
        exit(0)
    

