# OcGenerator

OcGenerator is a service for the conversion of music files to ocarina pictorial tablature. Created as part of my dissertation/final year project at [Aberystwyth University](https://www.aber.ac.uk/en/|). Currently
it supports .wav, .ogg, .mp3 and .webm formats.

### Library Usages
* Interface written in HTML5/CSS3, powered by [Flask](https://github.com/pallets/flask).
* Uses the excellent [Aubio](https://github.com/aubio/aubio) library for pitch detection and extraction.
* And the equally-excellent [Pillow](https://python-pillow.org/) for image segmentation and extraction

See my blog of my experience doing this project at my [blog!](http://rowansdissertation.blogspot.co.uk/|)

### Running Instructions:
* 'pip install -r requirements.txt'. THis will install all dependencies. This program has been developed on 3.5, and is incompatible with Python 2.
* Set PYTHONPATH to be the root directory of this program.
* 'export FLASK_APP=run.py'. This will set up Flasm on the correct file.
* 'flask run'. This will run the program on port 5000.
* Enjoy!

