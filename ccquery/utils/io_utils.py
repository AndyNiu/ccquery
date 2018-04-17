"""Execute useful file and folder commands"""

import os
import urllib
import bz2

from ccquery.error import ConfigError, DataError, CaughtException

def check_file_readable(input_file):
    """Check file existance"""
    if not os.path.exists(input_file):
        raise ConfigError(
            "File '{}' is missing or not readable".format(input_file))

def check_folder_readable(input_folder):
    """Check folder existance"""
    if not os.path.isdir(input_folder):
        raise ConfigError("Folder '{}' is missing".format(input_folder))

def create_folder(output):
    """Create folder path"""
    if not os.path.isdir(output):
        os.makedirs(output)

def create_path(output):
    """Create file path"""
    if not os.path.dirname(output):
        return
    if not os.path.isdir(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

def delete_file(input_file):
    """Delete file"""
    if os.path.exists(input_file):
        os.remove(input_file)

def filename(input_file):
    """Recover file name with extension"""
    return os.path.basename(input_file)

def filesize(input_file):
    """Recover a human readable file size"""

    check_file_readable(input_file)

    file_size = os.path.getsize(input_file)
    for count in ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
        if file_size > -1024.0 and file_size < 1024.0:
            return "{:3.1f}{}".format(file_size, count)
        file_size /= 1024.0
    return "{:.1f}?".format(file_size)

def count_lines(input_file):
    """Return the number of lines within a file"""

    check_file_readable(input_file)

    n = 0
    with open(input_file, 'r') as istream:
        for _ in istream:
            n += 1
    return n

def dirname(input_file):
    """Recover file dirname"""
    return os.path.dirname(input_file)

def basename(input_file):
    """Recover file basename"""
    return os.path.basename(os.path.splitext(input_file)[0])

def extension(input_file):
    """Recover file extension"""
    return os.path.splitext(input_file)[1]

def path_without_ext(input_file):
    """Recover path without extension"""
    return os.path.join(dirname(input_file), basename(input_file))

def has_extension(input_file, ext):
    """Check right file extension"""
    if input_file == '' or extension(input_file) != ext:
        return False
    return True

def change_extension(input_file, ext):
    """Change file extension into 'ext'"""
    if input_file == '':
        return ''
    return os.path.splitext(input_file)[0] + '.' + ext

def download(url, output):
    """Download gzip archive file from url and store its contents to file"""

    create_path(output)

    try:
        urllib.request.urlretrieve(url, output)
    except urllib.error.HTTPError as exc:
        raise CaughtException(
            "Exception encountered when retrieving data from '{}': {}".format(
                url, exc))

def decompress(path, output, blocksize=900*1024):
    """Download bz2 archive file from url and store its contents to file"""

    if not path.endswith('.bz2'):
        raise DataError("File '{}' is not a bz2 archive".format(path))

    create_path(output)
    with open(output, 'wb') as ostream:
        with open(path, 'rb') as istream:
            z = bz2.BZ2Decompressor()
            for block in iter(lambda: istream.read(blocksize), b''):
                ostream.write(z.decompress(block))
