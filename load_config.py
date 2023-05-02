""" Defines a function to load config yaml file into a global dictionary.
"""
import os
import yaml
import logging
import pathlib
from typing import Dict, Optional, Text

logger = logging.getLogger(__name__)


# Global dict to keep track of config yaml files that have been loaded.
preloaded_config = {}


def load_config(config_file: Text) -> Optional[Dict]:
    """ Load the config file into a global variable.

    Args:
        config_file: the configuration file path.
    Returns:
        None if config file not existing, Dictionary otherwise.
    """
    global preloaded_config

    # Get the path to the config file.
    config_path = config_file
    if not os.path.exists(config_path):
        return None

    # Key for dictionary = filename + timestamp.
    timestamp = str(pathlib.Path(config_path).stat().st_mtime)
    k = config_path + '_' + timestamp

    # Either we haven't loaded this file yet, or it's timestamp has changed.
    if k not in preloaded_config:
        preloaded_config[k] = {}
        logger.debug(f'Loading config file {config_path}')
        with open(config_path, 'rt', encoding='utf8') as config_file:
            preloaded_config[k] = yaml.load(config_file,
                                            Loader=yaml.FullLoader)

    return preloaded_config[k]
