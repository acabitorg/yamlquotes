# yamlquotes

### Store quote collections in YAML and render as PNG slideshow, MP4 video slideshow or booklet PDF for double-sided printing or reading

## Demos

* [Photo slideshow](https://photos.app.goo.gl/FQEYCPGZzbH589ns5)
* [Video slideshow](https://www.youtube.com/watch?v=zghmbdpZ14U)
* [PDF booklet noflip (for reading)](https://github.com/acabitorg/yamlquotes/blob/main/out/quotes-book-noflip.pdf)
* [PDF booklet flipped (for double-sided booklet printing)](https://github.com/acabitorg/yamlquotes/blob/main/out/quotes-book-flip.pdf)

## yamlquotes format

### A minimalist YAML-based file format for collections of quotations

Features:

* Quote text and metadata such as tags, content-warnings, author, date, language, translation, contextual info and geographic info
* [quotes.yml](quotes.yml) - an example yamlquotes file containing 500+ assorted quotes

## Disclaimer

The author(s) make no endorsement of the quotes contained in the example quotes.yml
file. Some of theses quotes are included purely for educational purposes, e.g. 
to dispell misconceptions about a diverse range of historical figures, good, evil 
and everywhere in between. Some quotes may be considered offensive when presented 
without context. Potentially offensive quotes may be tagged with appropriate 
content-warnings to enable filtering. Users are encouraged to create their own yamlquotes 
files. The quotes.yml file in this repo is only meant to serve as an example of the 
*yamlquotes* format.

# yamlquotes File Format

Every yamlquotes file has a top-level `quotes` list and also a top-level
`defaults` dictionary. All of the fields below are applicable at the individual 
quote level, and some may also be set in the `defaults`. `defaults` apply
only when that field is not overriden at the individual quote level.

Abbreviated field names are used to keep the yaml uncluttered and keep the 
file size low.

* `t` text of the quote
* `l` language of text (if different from default) in *ISO 639-2/T* format (e.g. `eng` for English, `fra` for French, `deu` for German etc.)
* `txr` translated text of the quote
* `a` author
* `ac` author contextual information (e.g. "Second President of the United States")
* `ayb` author year of birth 
* `ayd` author year of death
* `c` contextual information (in regard to the quote) (e.g. '"A Cult of Ignorance", Newsweek')
* `g` geographic information (location)
* `d` date (of the quote)
* `tags` category tags
* `cw` content-warning tags

Example quotes yml file with two quotes (one of which has a translation):
```
defaults:
  l: eng
quotes:
  - 
    t: Quidquid latine dictum sit, altum sonatur.
    txr: Whatever is said in Latin sounds profound.
    a: Anonymous
  - 
    t: >-
      Learning requires the humility to realize one
      has something to learn.
    a: Anonymous

```

### Content Warning Tags

Observe that some of the quotes may have `cw` (*content-warning*) tags. 
Users of this software could filter quotes based on these content-warning 
tags as desired by using the `--exclude-cw <cwlist>` or `--exclude-any-cw` 
command-line options. See below for examples.

E.g. if you want to generate a PDF for a youth audience, you can filter based
on the CW tags to generate a *clean* PDF.

### Quotation Marks
* Language affects quotation marks style (French guillements or English quotation marks)
* Translation quotation marks always use quotation marks style of default language.

# yamlquotes python package

## Python CLI for working with yamlquotes files and render as PNG slideshow, MP4 video slideshow or booklet PDF for double-sided printing or reading

### Features

* Validation
* Sorting
* Filtering based on quote metadata
* PDF output
* PDF booklet creation

### Dependencies

#### Python packages

* pyaml `pip install pyaml`
* pylatex  `pip install pylatex`
* PIL `pip install Pillow`

#### Linux packages

* Latex `sudo apt install texlive-latex-extra`
* pdfjam `sudo apt install pdfjam` (pdfjam is just a shell script wrapper for Latex)
* ffmpeg `sudo apt install ffmpeg`

### yamlquotes python CLI Reference

```
usage: __main__.py [-h] -f FILE [--include-tags INCLUDE_TAGS] [--exclude-tags EXCLUDE_TAGS] [--include-langs INCLUDE_LANGS] [--exclude-langs EXCLUDE_LANGS]
                   [--exclude-cw EXCLUDE_CW | --exclude-any-cw | --include-cw INCLUDE_CW] [--sort-by-author]
                   (--validate | --make-pdf | --make-pdf-book | --make-png-images | --make-png-video-frames | --save | --list-tags | --list-cw | --list-langs | --stats | --print) [--no-flip]

yamlquotes.py

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  <quotes_filename.yml>
  --include-tags INCLUDE_TAGS
                        Only include quotes with the specified tag(s) (command-separated values)
  --exclude-tags EXCLUDE_TAGS
                        Exclude quotes with the specified tag(s) (command-separated values) Takes precedence over --include-tags
  --include-langs INCLUDE_LANGS
                        Only include quotes in the specified language(s) (command-separated values)
  --exclude-langs EXCLUDE_LANGS
                        Exclude quotes in the specified language(s) (command-separated values) Takes precedence over --include-langs
  --exclude-cw EXCLUDE_CW
                        Exclude quotes with the specified content-warning(s) (command-separated values)
  --exclude-any-cw      Exclude quotes with any content-warnings
  --include-cw INCLUDE_CW
                        Only include quotes with the specified content-warning(s) (command-separated values)
  --sort-by-author      Sort output by author name, reversed
  --validate            Validate quotes yaml and exit
  --make-pdf            Make pdf from quotes yaml
  --make-pdf-book       Make pdf booklet from quotes yaml using pdfjam/pdfpages
  --make-png-images     Make png images from quotes yaml
  --make-png-video-frames
                        Make png video frames for ffmpeg from quotes yaml
  --save                Save sorted and/or filtered yaml to '.saved.yaml' file
  --list-tags           List all tags in the quotes file
  --list-cw             List all content-warnings in the quotes file
  --list-langs          List all languages in the quotes file
  --stats               Display statistics about the the quotes file
  --print               Print quotes
  --no-flip             Don't flip every other page vertically


```

The mode of operation is specified by one of the following mutually-exclusive arguments:

```
--validate | --make-pdf | --make-pdf-book | --make-png-images | --make-png-video-frames | --save | --list-tags | --list-cw | --list-langs | --stats | --print
```

### Usage Examples


###### Clean workspace

`make clean`


###### Make the full PDF booklet

I.e. generate `quotes.pdf` and then use `pdfjam` to convert it to a 2-up booklet (`quotes-book-[no]flip.pdf`)

```
make clean && python setup.py install
python -m yamlquotes -f quotes.yml --sort-by-author --make-pdf-book
```

Output: `quotes.pdf` and `quotes-book-[no]flip.pdf`

* `quotes.pdf` 1-UP (1 page per page) half-letter booklet PDF for reading e.g. on an e-reader.
* `quotes-book-flip.pdf` 2-UP (2 pages per printed page) half-letter booklet PDF with every other printed page flipped for double-sided printing. If you're trying to make a center-fold booklet, print this one.
* `quotes-book-noflip.pdf` 2-UP (2 pages per printed page) half-letter booklet PDF with no page-flipping for reading or single-sided printing.

Default is flipped (for double-sided printing). Add `--no-flip` if you want `noflip` (if you want a PDF for reading).

###### Make the full PDF but skip pdfjam booklet PDF conversion

```
make clean && python setup.py install
python -m yamlquotes -f quotes.yml --sort-by-author --make-pdf
```

Output: 

* `quotes.pdf` 1-UP PDF (half-letter paper size)

Note that the default paper size is half-letter (i.e. 5.5in x 8.5in, since it's meant to produce a PDF for input into pdfjam for conversion to a 2-up booklet PDF.


###### Validate yamlquotes file

```
$ python -m yamlquotes -f quotes.yml --validate
Valid
```

##### Basic examples

```

python -m yamlquotes -f quotes.yml --sort-by-author --make-pdf

python -m yamlquotes -f quotes.yml --sort-by-author --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --make-pdf-book --no-flip

python -m yamlquotes -f quotes.yml --sort-by-author --make-png-images

python -m yamlquotes -f quotes.yml --sort-by-author --make-png-video-frames

```


###### Advanced examples

```
python -m yamlquotes -f quotes.yml --sort-by-author --include-tags history --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --exclude-tags bible,politics --exclude-any-cw --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --include-tags bible --exclude-any-cw --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --exclude-tags bible --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --include-tags bible --exclude-tags new-testament --exclude-any-cw --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --include-tags history,philosophy,economics --exclude-any-cw --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --exclude-tags politics,economics,philosophy --exclude-any-cw --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --exclude-tags politics --exclude-cw racism,violence --make-pdf-book

python -m yamlquotes -f quotes.yml --sort-by-author --save
mv quotes.saved.yml quotes.yml


```


## Printing PDF Booklets

Tested using default GNOME PDF Document Viewer (Evince v40.1)

Requirements: A Linux-compatible printer that supports double-sided printing (tested using Brother HL-2270DW)

Evince PDF print setup:

If you are printing the `quotes-book-flip.pdf` PDF generated by yamlquotes.py, then every other page will already be flipped vertically for double-sided printing, so you should print as follows:

* Print > Page Setup
  * Layout > Two-Sided -> Long Edge (Standard)
  * Paper > Orientation > Landscape

If you are printing a booklet and the pages are not already flipped in the PDF (e.g. `quotes-book-noflip.pdf`), then you should choose "Short Edge (Flip)" to ensure that every other page is flipped vertically for double-sided printing:

* Print > Page Setup
  * Layout > Two-sided > Short Edge (Flip)
  * Paper > Orientation > Landscape

## Binding booklets

I highly recommend this YouTube video: [DIY Saddle Stitch Bookbinding Tutorial by Sea Lemon](https://www.youtube.com/watch?v=aWHkY5jOoqM). 

Required materials:

* A Linux-compatible printer that supports double-sided printing (tested using Brother HL-2270DW)
* Printer paper
* Toner cartridge
* Computer
* 11in x 8.5in cardstock
* Waxed thread
* Leather needles
* Awl
* Rubber mallet
* Flat board or two (that you don't mind getting gouged by the awl, can also be used for press)
* Book press (200+ lbs of weights or screw clamps)
* Optional: Paper guillotine

## PDF booklet conversion research notes


* `pdfbook2` is just a python wrapper for `pdfjam`. I ended up not using it.
* `pdfjam` is just a shell script wrapper for the `pdfpages` latex package. It's useful.

if run pdfjam with the following arguments:

`pdfjam --landscape --suffix book --booklet 'true' --paper letter --no-tidy --nup '2x1' -- quotes.pdf - `

then the following latex is generated (in `/tmp/pdfjam-...` folder, which persists if `--no-tidy` is specified):

```
\batchmode
\documentclass[letter,landscape]{article}
\usepackage[utf8]{inputenc}
\usepackage{pdfpages}

\begin{document}
\includepdfmerge[booklet=true,nup=2x1]{/tmp/pdfjam-B9JuuG/source-1.pdf,-}
\end{document}
```
