# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging

logger = logging.getLogger(__name__)

from .helpers import get_basename
from .pdf_maker import (make_pdf, make_pdf_book)
from .png_maker import (make_png_images)

class MakeArgsApplier():

    def __init__(self, args):
        self.args = args

    def apply(self, data):
        basename = get_basename(self.args)
        if self.args.make_pdf_book:
            make_pdf_book(data, basename, self.args.no_flip)
        elif self.args.make_pdf:
            make_pdf(data, basename)
        elif self.args.make_png_images:
            make_png_images(data, basename, video=False)
        elif self.args.make_png_video_frames:
            make_png_images(data, basename, video=True)
