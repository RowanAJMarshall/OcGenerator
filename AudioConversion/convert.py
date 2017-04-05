import pydub

from Utils import file_utilities
from Ocgen import ocgen

supported_formats = ('wav', 'mp3', 'webm', 'ogg')


class NotSupportedException(Exception):
    pass


# Converts the given file 'filepath' to the audio format 'format'
def convert(filepath: str, target_format: str) -> str:
    print(filepath)
    # if target_format not in supported_formats:
    #     raise NotSupportedException
    current_format = file_utilities.get_file_extension(filepath)
    _, new_filename = file_utilities.seperate_path_and_file(filepath.replace("." + current_format, "." + target_format))
    pydub.AudioSegment.from_file(filepath).export("static/" + new_filename, format=target_format)
    return None, new_filename


# Standardises given file to 'wav' so it can be transcribed
def standardise_format(filepath: str) -> str:
    return convert(filepath, 'wav')


def standardise_format1(filepath: str) -> str:
    if ocgen.check_format(filepath, 3) == "mp3":
        wav_filename = filepath.replace(".mp3", ".wav")
        pydub.AudioSegment.from_file(filepath).export(wav_filename, format='wav')
        return wav_filename
    elif ocgen.check_format(filepath, 3) == "ogg":
        wav_filename = filepath.replace(".ogg", ".wav")
        pydub.AudioSegment.from_file(filepath).export(wav_filename, format='wav')
        return wav_filename
    elif ocgen.check_format(filepath, 4) == "webm":
        wav_filename = filepath.replace(".webm", ".wav")
        pydub.AudioSegment.from_file(filepath).export(wav_filename, format='wav')
        return wav_filename
    return filepath