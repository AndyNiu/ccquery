"""Execute useful configuration commands"""

import collections
import yaml

from ccquery.utils import io_utils
from ccquery.error import ConfigError, CaughtException

def load_configuration(path):
    """Load configuration from yaml file"""

    io_utils.check_file_readable(path)

    conf = {}
    with open(path, 'r') as stream:
        try:
            conf = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise CaughtException(
                "Exception encountered during YAML load: {}".format(exc))

    if not conf:
        raise ConfigError("Empty configuration in '{}'".format(path))
    if not isinstance(conf, dict):
        raise ConfigError("Not a dict object stored in '{}'".format(path))

    return conf

def nested_keys_iter(d):
    for key, value in d.items():
        if isinstance(value, collections.Mapping):
            for inner_key in nested_keys_iter(value):
                yield inner_key
        else:
            yield key

def get_missing(rlist, clist):
    missing = []
    for key in rlist:
        if key not in clist:
            missing.append(key)
    return missing

def match_keys_structure(config, reference):
    """Match configuration structure with expected structure"""

    cstruct = sorted(list(nested_keys_iter(config)))
    rstruct = sorted(list(nested_keys_iter(reference)))
    missing = get_missing(rstruct, cstruct)

    if missing:
        raise ConfigError(
            "Given configuration {} has following missing keys {}"\
            "compared to the expected structure {}"\
            .format(config, missing, reference))

def match_keys(config, reference):
    """Match first-level keys between two dictionaries"""

    ckeys = sorted(list(config.keys()))
    missing = get_missing(reference, ckeys)

    if missing:
        raise ConfigError("Missing mandatory options {}".format(missing))

def expand_to_string(config):
    """Return a string expanding the configuration"""

    if not isinstance(config, list):
        return ''

    sconf = ''
    for item in config:
        if isinstance(item, str):
            sconf += item + ' '
        elif isinstance(item, dict):
            for key, value in item.items():
                sconf += "{} {} ".format(key, value)
        elif isinstance(item, list):
            for key in item:
                sconf += "{} ".format(key)

    return sconf.strip()
