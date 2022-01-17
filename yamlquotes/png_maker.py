# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import math
import os

from .constants import OUTDIR
from .helpers import get_defaults
from .image_utils import ImageText
from .repr_quote_plaintext import repr_quote_plaintext

logger = logging.getLogger(__name__)

FONT_SCALE_FRAME_MULTIPLIER = 2 # multiplies the effect of the font-scaling
# on the video duration (smaller font-size = more video frames = longer reading time)
MIN_VIDEO_FRAMES = 12 # effectively, the minimum display time in seconds
# (assuming using ffmpeg -r 1 to get a frame rate of 1 fps)

def make_png_image_autoscale_text(text, quote_name, output_dir, 
        background, color, font_filename, font_size,
        position, alignment, resolution, video, start_frame_number):
    box_width = resolution[0] - 180
    max_height = resolution[1] - position[1]
    it = None
    scaled_font_size = font_size
    while scaled_font_size > 2:
        it = ImageText(resolution, background=background)

        width, height = it.write_text_box(position, text, 
            box_width=box_width, font_filename=font_filename, 
            font_size=scaled_font_size, color=color, place=alignment)
        logger.debug('quote_name: {} height: {}'.format(quote_name, height))
        if height < max_height:
            break
        scaled_font_size -= 2
    frame_count = 1
    if video:
        # smaller font-size = longer reading time = more video frames
        font_scale = font_size - scaled_font_size # inverse relationsip
        frame_count = int(math.ceil(MIN_VIDEO_FRAMES + (font_scale * FONT_SCALE_FRAME_MULTIPLIER)))
    logger.debug(f'quote_name: {quote_name} frame_count: {frame_count}')
    frames_saved = 0
    for i in range(frame_count):
        frame_number = start_frame_number + i
        png_fname = os.path.join(output_dir, f'quote_{frame_number:06}.png')
        it.save(png_fname)
        logger.debug(f'saved frame {png_fname}')
        frames_saved += 1
    return frames_saved

def make_png_images_autoscale_text(data, defaults, output_dir, 
        background, color, font_filename, font_size, 
        position, alignment, resolution, video):
    frame_number = 1
    for i, qt in enumerate(data['quotes']):
        text = repr_quote_plaintext(qt, defaults)
        quote_name = f'quote_{i+1:06}'
        frame_number += make_png_image_autoscale_text(text, quote_name, output_dir, 
            background, color, font_filename, font_size,
            position, alignment, resolution, video, frame_number)
    if video:
        cmd = r'ffmpeg -r 1 -f image2 -s 1280x720 -i ' + \
            output_dir + r'/quote_%06d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ' + \
            output_dir + r'/quotes.mp4'
        logger.debug(f'video cmd: {cmd}')
        os.system(cmd)

def make_png_images(data, name, video):
    logger.debug('name: {}'.format(name))
    defaults = get_defaults(data)
    output_dir = os.path.join(OUTDIR, '{}-png'.format(name))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    background = (0, 0, 0, 255)
    color = (255, 255, 255)
    font_filename = os.path.join('ttf', 'DejaVuSerif.ttf')
    font_size = 48
    position = (40, 40)
    alignment = 'left'
    resolution = (1280, 720)
    make_png_images_autoscale_text(data, defaults, output_dir,
        background, color, font_filename, font_size,
        position, alignment, resolution, video)
