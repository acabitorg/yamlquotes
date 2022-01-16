all: pdf pdf-book pdf-book-noflip png-images

quotes = yamlquotes/data/quotes.yml

build:
	python setup.py develop

pdf: build
	python -m yamlquotes -f $(quotes) --sort-by-author --make-pdf

pdf-book: build
	python -m yamlquotes -f $(quotes) --sort-by-author --make-pdf-book

pdf-book-noflip: build
	python -m yamlquotes -f $(quotes) --sort-by-author --make-pdf-book --no-flip

png-images: build
	python -m yamlquotes -f $(quotes) --sort-by-author --make-png-images

png-video-frames: build
	python -m yamlquotes -f $(quotes) --sort-by-author --make-png-video-frames

clean:
	rm -rf out
	rm -f log/*.log*
	rm -rf __pycache__
