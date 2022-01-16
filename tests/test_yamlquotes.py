import pytest
import os

@pytest.fixture(scope="module")
def setup():
    os.system('make clean')

def test_pdf(setup):
    assert os.system('./yamlquotes.py -f quotes.yml --sort-by-author --make-pdf') == 0

def test_pdf_book(setup):
    assert os.system('./yamlquotes.py -f quotes.yml --sort-by-author --make-pdf-book') == 0

def test_pdf_book_noflip(setup):
    assert os.system('./yamlquotes.py -f quotes.yml --sort-by-author --make-pdf-book --no-flip') == 0

def test_png(setup):
    assert os.system('./yamlquotes.py -f quotes.yml --sort-by-author --make-png') == 0
