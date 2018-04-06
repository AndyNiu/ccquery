import logging
import pandas as pd
import fastText

from ccquery.utils import io_utils, str_utils
from ccquery.error import DataError, ConfigError

LOGGER = logging.getLogger(__name__)

def load(path, header=None, names=None, sep=',', fields=None):
    """Load entire data"""

    if fields:
        LOGGER.info("Load {} columns from '{}' csv file".format(fields, path))
    else:
        LOGGER.info("Load data from '{}' csv file".format(path))

    io_utils.check_file_readable(path)
    with open(path, 'r', encoding='utf-8') as istream:
        data = pd.read_csv(
            istream,
            usecols=fields,
            header=header,
            names=names,
            sep=sep,
            encoding='utf-8')

    if data.empty:
        LOGGER.warning('No data found')
    else:
        LOGGER.info("Loaded {} entries".format(len(data)))

    return data

def load_chunk(path, nrows, header=None, names=None, sep=',', to_shuffle=False):
    """Load 'nrows' entries from the file"""

    data = load(path, header=header, names=names, sep=sep)

    LOGGER.info("Return {} entries".format(nrows))
    if not to_shuffle:
        return data.iloc[:nrows]
    return data.sample(nrows)

def stream(path, chunksize=1, header=None, names=None, sep=','):
    """Iterate through the data, one chunk at a time"""

    io_utils.check_file_readable(path)
    return pd.read_csv(
        path,
        iterator=True,
        chunksize=chunksize,
        header=header,
        names=names,
        sep=sep,
        encoding='utf-8')

def stream_field(path, field, header=None, names=None, sep=','):
    """Iterate through the 'field' data, one chunk at a time"""

    io_utils.check_file_readable(path)

    with open(path, 'r', encoding='utf-8') as istream:
        for entry in pd.read_csv(
                istream,
                usecols=[field],
                header=header,
                iterator=True,
                chunksize=1,
                names=names,
                sep=sep,
                encoding='utf-8'):
            for _, value in entry[field].iteritems():
                yield value

def filter_data(data, filters=None, fields=None, langdetect=None, clean=None):
    """Return only rows matching given filters"""

    cdata = data.copy()

    if filters:
        LOGGER.info("Process filters={}".format(filters))
        for field, value in filters.items():
            if field in cdata.columns:
                cdata = cdata[cdata[field] == value]

    if fields:
        for field in fields.values():
            if field not in cdata.columns:
                raise DataError(
                    "Column {} missing in data {}".format(field, cdata.columns))
        LOGGER.info("Select columns={}".format(fields))
        cdata = cdata[list(fields.values())]

    if langdetect:
        LOGGER.info("Apply language detection: {}".format(langdetect))
        field = langdetect['field']

        if field not in cdata.columns:
            raise DataError(
                "Column {} missing in data {}".format(field, cdata.columns))

        lang = langdetect['language']
        classifier = fastText.load_model(langdetect['model'])

        drop_indexes = []
        for index, value in cdata[field].iteritems():
            prediction = classifier.predict(str(value))
            if prediction:
                prediction = prediction[0][0][-2:]
            if prediction != lang:
                drop_indexes.append(index)

        if drop_indexes:
            cdata = cdata.drop(drop_indexes)

    LOGGER.info("Return {} entries after language detection".format(len(cdata)))

    if clean:
        LOGGER.info('Clean queries: remove unwanted characters')

        if not fields:
            raise ConfigError("Cleaning requires the 'fields' configuration")

        input_cleaner = getattr(str_utils, clean['input']['method'])
        input_kwargs = clean['input'].get('kwargs', {})

        target_cleaner = getattr(str_utils, clean['target']['method'])
        target_kwargs = clean['target'].get('kwargs', {})

        drop_indexes = set()
        for index, row in cdata.iterrows():
            for ftype, column in fields.items():
                if ftype == 'input':
                    clean_text = input_cleaner(row[column], **input_kwargs)
                elif ftype == 'target':
                    clean_text = target_cleaner(row[column], **target_kwargs)
                else:
                    raise ConfigError("Unknown given field {}".format(ftype))

                if clean_text:
                    cdata.at[index, column] = clean_text
                else:
                    drop_indexes.add(index)

        if drop_indexes:
            cdata = cdata.drop(drop_indexes)

    LOGGER.info("Return {} entries after character cleanup".format(len(cdata)))
    return cdata

def store_csv(data, output, quoting=1):
    """Store data to csv file"""

    LOGGER.info("Store data to '{}' csv file".format(output))

    io_utils.create_path(output)
    with open(output, 'w', encoding='utf-8') as ostream:
        data.to_csv(ostream, index=0, header=1, quoting=quoting)

def store_jsonlines(data, output):
    """Store data to json file"""

    LOGGER.info("Store data to '{}' json file".format(output))

    io_utils.create_path(output)
    with open(output, 'w', encoding='utf-8') as ostream:
        for _, row in data.iterrows():
            ostream.write(row.to_json(force_ascii=False) + '\n')
