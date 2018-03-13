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

    if not isinstance(conf, dict):
        raise ConfigError("Not a dict object stored in '{}'".format(path))
    if not conf:
        raise ConfigError("Empty configuration in '{}'".format(path))

    return conf

def nested_keys_iter(d):
    for key, value in d.items():
        if isinstance(value, collections.Mapping):
            for inner_key in nested_keys_iter(value):
                yield inner_key
        else:
            yield key

def check_presence(clist, rlist):
    missing = []
    for key in rlist:
        if key not in clist:
            missing.append(key)
    return missing

def match_keys_structure(config, reference):
    """Match configuration structure with expected structure"""

    cstruct = sorted(list(nested_keys_iter(config)))
    rstruct = sorted(list(nested_keys_iter(reference)))
    missing = check_presence(cstruct, rstruct)

    if missing:
        raise ConfigError(
            "Given configuration {} has following missing keys {}"\
            "compared to the expected structure {}"\
            .format(config, missing, reference))

def match_keys(config, reference):
    """Match first-level keys between two dictionaries"""

    ckeys = sorted(list(config.keys()))
    missing = check_presence(ckeys, reference)

    if missing:
        raise ConfigError("Missing mandatory options {}".format(missing))
