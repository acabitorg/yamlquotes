all: pdf pdf-book pdf-book-noflip png-images

quotes = yamlquotes/data/quotes.yml
filter = --include-tags anarchism

build:
	python setup.py develop

pdf: build
	python -m yamlquotes -f $(quotes) --sort-by-author $(filter) --make-pdf

pdf-book: build
	python -m yamlquotes -f $(quotes) --sort-by-author $(filter) --make-pdf-book

pdf-book-noflip: build
	python -m yamlquotes -f $(quotes) --sort-by-author $(filter) --make-pdf-book --no-flip

png-images: build
	python -m yamlquotes -f $(quotes) --sort-by-author $(filter) --make-png-images

png-video-frames: build
	python -m yamlquotes -f $(quotes) --sort-by-author $(filter) --make-png-video-frames

clean:
	rm -rf out
	rm -f log/*.log*
	rm -rf __pycache__
	pip uninstall -y yamlquotes
