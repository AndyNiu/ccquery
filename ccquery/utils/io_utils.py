"""Execute useful file and folder commands"""

import os.path
from ccquery.error import ConfigError

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

def filename(input_file):
    """Recover file name with extension"""
    return os.path.basename(input_file)

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
