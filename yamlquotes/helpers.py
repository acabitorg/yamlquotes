# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

from os.path import (splitext, basename)

def get_basename(args):
	return splitext(basename(args.file))[0]
