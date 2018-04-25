import random
import logging
from ccquery.utils import io_utils

LOGGER = logging.getLogger(__name__)

def load(path):
    """Load entire data"""

    LOGGER.info("Load data from '{}' text file".format(path))
    io_utils.check_file_readable(path)

    data = []
    with open(path, 'r', encoding='utf-8') as istream:
        for line in istream:
            data.append(line.strip())

    LOGGER.info("Loaded {} sentences".format(len(data)))
    return data

def load_chunk(path, n=100, to_shuffle=False):
    """Load first 'n' entries from the file"""

    data = load(path)
    if not to_shuffle:
        return data[:n]
    return random.sample(data, n)

def stream(path):
    """Iterate through the data, one entry at a time"""

    io_utils.check_file_readable(path)
    with open(path, 'r', encoding='utf-8') as istream:
        for line in istream:
            line = line.strip()
            yield line

def stream_chunk(path, n=100):
    """Iterate through the data, one chunk at a time"""

    io_utils.check_file_readable(path)
    with open(path, 'r', encoding='utf-8') as istream:
        data = []
        for line in istream:
            line = line.strip()
            data.append(line)
            if len(data) == n:
                yield data
                data = []
