import hashlib
import time


def get_file_extension(filepath):
    extension = ""
    for char in filepath[::-1]:
        if char == ".":
            return extension[::-1]
        else:
            extension += char
    return extension[::-1]


def generate_filename(filename):
    string_to_hash = filename + str(time.time())
    hashed_val = hashlib.sha1(bytes(string_to_hash, encoding='utf-8'))
    return hashed_val.hexdigest()


def seperate_path_and_file(filepath) -> (str, str):
    slash_encountered = False
    path = ""
    filename = ""
    for char in filepath[::-1]:
        if char == "/":
            slash_encountered = True
            path += char
        elif not slash_encountered:
            filename += char
        else:
            path += char
    return path[::-1], filename[::-1]