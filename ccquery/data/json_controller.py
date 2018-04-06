import json
import types
import logging
import numpy as np

from ccquery.utils import io_utils

LOGGER = logging.getLogger(__name__)

def load_field(path, field):
    """Load data for specific field"""

    LOGGER.info("Load data from '{}' json file".format(path))
    io_utils.check_file_readable(path)

    data = []
    with open(path, 'r', encoding='utf-8') as istream:
        for line in istream:
            entry = json.loads(line)
            if field in entry:
                data.append(entry[field])
    if data:
        LOGGER.info("Loaded {} entries".format(len(data)))
    else:
        LOGGER.warning("No entries found for field={}".format(field))

    return data

def load_fields(path, fields):
    """Load data for specific fields"""

    LOGGER.info("Load data from '{}' json file".format(path))
    io_utils.check_file_readable(path)

    data = {field:[] for field in fields}
    with open(path, 'r', encoding='utf-8') as istream:
        for line in istream:
            entry = json.loads(line)
            for field in fields:
                if field in entry:
                    data[field].append(entry[field])
    for field in fields:
        if data[field]:
            LOGGER.info("Loaded {} entries for field={}".format(
                len(data), field))
        else:
            LOGGER.warning("No entries found for field={}".format(field))

    return data

def load(path, input_field='noisy', target_field='clean'):
    """Load data for specific input and output fields"""

    # load two arrays
    data = load_fields(path, [input_field, target_field])
    return data[input_field], data[target_field]

def load_chunk(
        path, n, input_field='noisy', target_field='clean', to_shuffle=False):
    """Load 'n' entries from the file"""

    input_seqs, output_seqs = load(path, input_field, target_field)

    LOGGER.info("Return only {} entries".format(n))
    if not to_shuffle:
        return input_seqs[:n], output_seqs[:n]

    index = np.random.choice(range(0, len(input_seqs), n, replace=False))
    return [input_seqs[i] for i in index], [output_seqs[i] for i in index]

def stream_field(path, field):
    """Iterate through the data, one entry at a time"""

    io_utils.check_file_readable(path)
    with open(path, 'r', encoding='utf-8') as istream:
        for line in istream:
            entry = json.loads(line)
            yield entry[field]

def stream(path, input_field='noisy', target_field='clean'):
    """Iterate through the data, one entry at a time"""

    io_utils.check_file_readable(path)
    with open(path, 'r', encoding='utf-8') as istream:
        for line in istream:
            entry = json.loads(line)
            yield entry[input_field], entry[target_field]

def stream_chunk(path, n, input_field='noisy', target_field='clean'):
    """Iterate through the data, one chunk at a time"""

    io_utils.check_file_readable(path)
    with open(path, 'r', encoding='utf-8') as istream:
        input_seqs, output_seqs = [], []
        for line in istream:
            entry = json.loads(line)
            input_seqs.append(entry[input_field])
            output_seqs.append(entry[target_field])
            if len(input_seqs) == n:
                yield input_seqs, output_seqs
                input_seqs, output_seqs = [], []

def store_text(data, output):
    """Store single-field data to text file"""

    if not isinstance(data, list) \
            and not isinstance(data, types.GeneratorType):
        LOGGER.warning(
            "Method expects a list or a generator object instead of {}".format(
                data.__class__))
        return

    LOGGER.info("Store data to '{}' text file".format(output))
    io_utils.create_path(output)
    with open(output, 'w', encoding='utf-8') as ostream:
        for entry in data:
            ostream.write(entry + '\n')
