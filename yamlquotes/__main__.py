# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import argparse
import codecs
import logging.config
import logging
import math
import os
from pylatex import (
    Command, Document, LineBreak, MiniPage, 
    Section, Subsection, TextBlock)
from pylatex.utils import italic, NoEscape
import sys
assert sys.version_info >= (3, 9)
import yaml
from yaml.representer import SafeRepresenter

from .constants import (EM_DASH, OUTDIR)
from .image_utils import ImageText
from .load_quotes import load_quotes
from .save_quotes import save_quotes
from .validate_quotes import validate_quotes

with open('logging.yml','rt') as f:
    config=yaml.safe_load(f.read())
    f.close()
logging.config.dictConfig(config)
logger = logging.getLogger('yamlquotes.py')

parser = argparse.ArgumentParser(description='yamlquotes.py')

#input:
parser.add_argument('-f', '--file', type=str,
                    help='<quotes_filename.yml>', required=True)

#filter modifiers:
parser.add_argument('--include-tags', type=str, \
    help='Only include quotes with the specified tag(s) (command-separated values)')
parser.add_argument('--exclude-tags', type=str, \
    help='Exclude quotes with the specified tag(s) (command-separated values) ' + \
    'Takes precedence over --include-tags')

parser.add_argument('--include-langs', type=str, \
    help='Only include quotes in the specified language(s) (command-separated values)')
parser.add_argument('--exclude-langs', type=str, \
    help='Exclude quotes in the specified language(s) (command-separated values) ' + \
    'Takes precedence over --include-langs')

cw_group = parser.add_mutually_exclusive_group()
cw_group.add_argument('--exclude-cw', type=str, \
    help='Exclude quotes with the specified content-warning(s) (command-separated values)')
cw_group.add_argument('--exclude-any-cw', action='store_true', \
    help='Exclude quotes with any content-warnings')
cw_group.add_argument('--include-cw', type=str, \
    help='Only include quotes with the specified content-warning(s) (command-separated values)')

#sort modifiers:
parser.add_argument('--sort-by-author', action='store_true', \
    help='Sort output by author name, reversed')

#operation:
oper_group = parser.add_mutually_exclusive_group(required=True)

oper_group.add_argument('--validate', action='store_true', \
    help='Validate quotes yaml and exit')

oper_group.add_argument('--make-pdf', action='store_true', \
    help='Make pdf from quotes yaml')
oper_group.add_argument('--make-pdf-book', action='store_true', \
    help='Make pdf booklet from quotes yaml using pdfjam/pdfpages')
oper_group.add_argument('--make-png-images', action='store_true', \
    help='Make png images from quotes yaml')
oper_group.add_argument('--make-png-video-frames', action='store_true', \
    help='Make png video frames for ffmpeg from quotes yaml')

oper_group.add_argument('--save-sorted', action='store_true', \
    help='Save sorted yaml to \'_sorted.yaml\' file')

oper_group.add_argument('--list-tags', action='store_true', \
    help='List all tags in the quotes file')
oper_group.add_argument('--list-cw', action='store_true', \
    help='List all content-warnings in the quotes file')
oper_group.add_argument('--list-langs', action='store_true', \
    help='List all languages in the quotes file')

oper_group.add_argument('--stats', action='store_true', \
    help='Display statistics about the the quotes file')
oper_group.add_argument('--print', action='store_true', \
    help='Print quotes')

#operation modifiers:
parser.add_argument('--no-flip', action='store_true', default=False, \
    help='Don\'t flip every other page vertically')

args = parser.parse_args()

exclude_cw = []
include_cw = []
exclude_tags = [] 
include_tags = []
exclude_langs = []
include_langs = []

if args.exclude_cw != None:
    exclude_cw += args.exclude_cw.split(',')
if args.include_cw != None:
    include_cw += args.include_cw.split(',')
if args.exclude_tags != None:
    exclude_tags += args.exclude_tags.split(',')
if args.include_tags != None:
    include_tags += args.include_tags.split(',')
if args.exclude_langs != None:
    exclude_langs += args.exclude_langs.split(',')
if args.include_langs != None:
    include_langs += args.include_langs.split(',')

if set(include_tags) & set(exclude_tags):
    logger.error('--include-tags and --exclude-tags must\'t overlap, ya doofus')
    print_usage()
    sys.exit(1)

if set(include_langs) & set(exclude_langs):
    logger.error('--include-langs and --exclude-langs must\'t overlap, ya ding dong')
    print_usage()
    sys.exit(1)

def get_qt_prop_type(prop_name):
    if prop_name == 'cw' or prop_name == 'tags':
        return 'list'
    return 'str'

def append_mp(mp, doc):
    mp.append(LineBreak())
    mp.append(NoEscape(r'\vspace{1mm}'))
    doc.append(mp)
    doc.append(LineBreak())
    doc.append(NoEscape(r'\vspace{1mm}'))

def get_qt_beg(l):
    if l == 'fra':
        return '«\u00A0'
    else:
        return '“'

def get_qt_end(l):
    if l == 'fra':
        return '\u00A0»'
    else:
        return '”'

def expand_markup(t):
    return t.replace('--', EM_DASH)

def format_text(t, l):
    return get_qt_beg(l) + expand_markup(t.rstrip()) + get_qt_end(l)

def get_lang(qt, defaults):
    l = defaults['l']
    if 'l' in qt:
        l = qt['l']    
    return l

def mp_append_t(mp, qt, defaults):
    mp.append(format_text(qt['t'], get_lang(qt, defaults)))
    mp.append(LineBreak())
    mp.append(NoEscape(r'\vspace{1mm}'))

def get_t(qt, defaults):
    txt = ''
    txt += format_text(qt['t'], get_lang(qt, defaults))
    txt += '\n'
    return txt

def mp_append_txr(mp, qt, defaults):
    if 'txr' in qt:
        #translation quotation marks always conform to default language
        mp.append(format_text(qt['txr'], defaults['l']))
        mp.append(LineBreak()) 

def get_txr(qt, defaults):
    txt = ''
    if 'txr' in qt:
        #translation quotation marks always conform to default language
        txt += format_text(qt['txr'], defaults['l'])
        txt += '\n'
    return txt

def mp_append_a(mp, qt, defaults):
    mp.append(EM_DASH + qt['a'])

def get_a(qt, defaults):
    return EM_DASH + qt['a']

def mp_append_ac(mp, qt, defaults):
    if 'ac' in qt:
        mp.append(NoEscape(', \\textit{{{}}}'.format(qt['ac'].rstrip())))   

def get_ac(qt, defaults):
    txt = ''
    if 'ac' in qt:
        txt += ', {}'.format(qt['ac'].rstrip())
    return txt

def mp_append_d(mp, qt, defaults):
    if 'd' in qt:
        field_d = str(qt['d'])
        mp.append(', ' + field_d)

def get_d(qt, defaults):
    txt = ''
    if 'd' in qt:
        field_d = str(qt['d'])
        txt += ', ' + field_d
    return txt

def mp_append_c(mp, qt, defaults):
    if 'c' in qt:
        mp.append(NoEscape(', \\textit{{{}}}'.format(qt['c'].rstrip())))    

def get_c(qt, defaults):
    txt = ''
    if 'c' in qt:
        txt += ', {}'.format(qt['c'].rstrip())
    return txt

def mp_append_g(mp, qt, defaults):
    if 'g' in qt:
        field_g = qt['g']
        mp.append(', ' + field_g)

def get_g(qt, defaults):
    txt = ''
    if 'g' in qt:
        field_g = qt['g']
        txt += ', ' + field_g
    return txt

def repr_quote_pylatex_minipage(qt, defaults):
    mp = MiniPage(align='l')
    mp_append_t(mp, qt, defaults)
    mp_append_txr(mp, qt, defaults)
    mp_append_a(mp, qt, defaults)
    mp_append_ac(mp, qt, defaults)
    mp_append_c(mp, qt, defaults)
    mp_append_d(mp, qt, defaults)
    mp_append_g(mp, qt, defaults)
    return mp

def repr_quote_plaintext(qt, defaults):
    txt = ''
    txt += get_t(qt, defaults)
    txt += get_txr(qt, defaults)
    txt += get_a(qt, defaults)
    txt += get_ac(qt, defaults)
    txt += get_c(qt, defaults)
    txt += get_d(qt, defaults)
    txt += get_g(qt, defaults)
    return txt


def qt_key_rauthor(qt):
    """Key function to sort by author name reversed
    E.g. 'Dwight D. Eisenhower'.split()[::-1]
    ['Eisenhower', 'D.', 'Dwight']
    """
    return qt['a'].split()[::-1]

def get_defaults(data):
    defaults = {'l':'eng'}
    if 'defaults' in data:
        defaults = data['defaults']
    return defaults

def fill_document(data, doc): 
    with doc.create(Section('Selected Quotes')):
        for qt in data['quotes']:
            mp = repr_quote_pylatex_minipage(qt, get_defaults(data))
            append_mp(mp, doc);

def convert_pdf_to_booklet_pdfjam(name):
    infile = os.path.join(OUTDIR, "{}.pdf".format(name))
    suffix = 'book'
    pdfjam_args = '--booklet true '
    if args.no_flip:
        pdfjam_args = '--no-twoside '
        suffix += '-noflip'
    else:
        suffix += '-flip'
    cmd = "pdfjam --landscape --outfile {} --suffix {} " \
        .format(OUTDIR, suffix) + \
        "--paper letter --no-tidy --nup 2x1 --scale 1.0 {} {}" \
        .format(pdfjam_args, infile)
    logger.debug('cmd: %s', cmd)
    if os.system(cmd) != 0:
        sys.exit(1)

def make_pdf(data, name):
    """Note that a 1in margin translates to a 0.5in margin in the 2-up booklet"""
    logger.debug(f'make_pdf name={name}')
    geometry_options = {
        'tmargin': '0.75in',
        'bmargin': '0.75in',
        'lmargin': '0.75in',
        'rmargin': '0.75in',
        'paperheight': '8.5in',
        'paperwidth': '5.5in'
    }
    default_filepath = os.path.join(OUTDIR, name)
    logger.debug(f'default_filepath={default_filepath}')
    doc = Document(default_filepath, geometry_options=geometry_options, font_size='large')

    fill_document(data, doc)
    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()

def make_pdf_book(data, name):
    logger.debug(f'make_pdf_book name={name}')
    make_pdf(data, name)
    convert_pdf_to_booklet_pdfjam(name)

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

def _list_qt_prop_vals(data, prop_name):
    vals = set()
    for qt in data['quotes']:
        if prop_name in qt:
            if get_qt_prop_type(prop_name) == 'list':
                vals.update(qt[prop_name])
            else:
                vals.add(qt[prop_name])
    logger.debug('\n'.join(vals))

def list_cw(data):
    _list_qt_prop_vals(data, 'cw')

def list_langs(data):
    _list_qt_prop_vals(data, 'l')

def list_tags(data):
    _list_qt_prop_vals(data, 'tags')


def apply_exclude_any_cw_filter(data):
    if not args.exclude_any_cw:
        return
    data['quotes'] = \
        [qt for qt in data['quotes'] if 'cw' not in 'qt']

def get_exclude_list(prop_name):
    if prop_name == 'cw':
        return exclude_cw
    elif prop_name == 'langs':
        return exclude_langs
    elif prop_name == 'tags':
        return exclude_tags
    sys.exit(1)

def get_include_list(prop_name):
    if prop_name == 'cw':
        return include_cw
    elif prop_name == 'langs':
        return include_langs
    elif prop_name == 'tags':
        return include_tags
    sys.exit(1)

def apply_exclude_filter(data, prop_name):
    quotes = []
    exclude_list = get_exclude_list(prop_name)
    for qt in data['quotes']:
        if prop_name in qt and \
        set(qt[prop_name]) & set(exclude_list):
            continue
        quotes.append(qt)
    data['quotes'] = quotes

def apply_include_filter(data, prop_name):
    quotes = []
    include_list = get_include_list(prop_name)
    for qt in data['quotes']:
        if len(include_list) > 0:
            if prop_name in qt:
                if not set(qt[prop_name]) & \
                set(include_list):
                    continue
            else:
                continue
        quotes.append(qt)
    data['quotes'] = quotes


def apply_exclude_cw_filters(data):
    apply_exclude_filter(data, 'cw')

def apply_exclude_tag_filters(data):
    apply_exclude_filter(data, 'tags')

def apply_exclude_lang_filters(data):
    apply_exclude_filter(data, 'langs')


def apply_include_cw_filters(data):
    apply_include_filter(data, 'cw')

def apply_include_lang_filters(data):
    apply_include_filter(data, 'langs')

def apply_include_tag_filters(data):
    apply_include_filter(data, 'tags')


def print_stats(data):
    quotes = data['quotes']
    count = len(quotes)
    print("count={}".format(count))

def print_quotes(data):
    quotes = data['quotes']
    for i, qt in enumerate(quotes):
        print('{}: {}'.format(i+1, qt))

def save_sorted(data, basename):
    save_quotes(data, basename)


def apply_filter_args(data):
    apply_exclude_cw_filters(data)
    apply_include_cw_filters(data)
    apply_exclude_any_cw_filter(data)
    apply_exclude_tag_filters(data)
    apply_include_tag_filters(data)
    apply_exclude_lang_filters(data)
    apply_include_lang_filters(data)

def apply_sort_args(data):
    if args.sort_by_author:
        data['quotes'] = sorted(data['quotes'], key=qt_key_rauthor)


def main():
    basename = \
        os.path.splitext(os.path.basename(args.file))[0]

    logger.debug(f'basename={basename}')
    data = load_quotes(args.file)

    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    validate_quotes(data)
    if args.validate:
        print('Valid')
        sys.exit(0)

    apply_sort_args(data)
    if args.save_sorted:
        save_sorted(data, basename)
        sys.exit(0)

    apply_filter_args(data)

    if args.stats:
        print_stats(data) 
    elif args.print:
        print_quotes(data)
    elif args.make_pdf_book:
        make_pdf_book(data, basename)
    elif args.make_pdf:
        make_pdf(data, basename)
    elif args.make_png_images:
        make_png_images(data, basename, video=False)
    elif args.make_png_video_frames:
        make_png_images(data, basename, video=True)
    elif args.list_cw:
        list_cw(data)
    elif args.list_langs:
        list_langs(data)
    elif args.list_tags:
        list_tags(data)

if __name__ == '__main__':
    main()
