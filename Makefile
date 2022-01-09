all: pdf pdf-book pdf-book-noflip png-images

pdf:
	./yamlquotes.py -f quotes.yml --sort-by-author --make-pdf

pdf-book:
	./yamlquotes.py -f quotes.yml --sort-by-author --make-pdf-book

pdf-book-noflip:
	./yamlquotes.py -f quotes.yml --sort-by-author --make-pdf-book --no-flip

png-images:
	./yamlquotes.py -f quotes.yml --sort-by-author --make-png-images

png-video-frames:
	./yamlquotes.py -f quotes.yml --sort-by-author --make-png-video-frames

clean:
	rm -rf out
	rm -f log/*.log*
	rm -rf __pycache__
