# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import yaml
from yaml.representer import SafeRepresenter

def load_quotes(yaml_fname):
    data = None
    with open(yaml_fname, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)
            sys.exit(1)
    return data
