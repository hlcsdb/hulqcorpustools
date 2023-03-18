# hulqtransliterator
transliterate from one way of writing hul’q’umi’num’ to another

I'll write more later 😇

## NEW FEATURES TO IMPLEMENT:
### REAL FEATURES:
- [ ] get the standalone executable to work ([py2app](https://github.com/ronaldoussoren/py2app) please....)
- [ ] drag and drop file onto .app or whatever instead of using the file browser
- [ ] working robust command-line interface

### NEW FEATURES?!:
- [x] instant transliterator that transliterates on keypress
    - [x] use same engine as file transliterator
- [x] replace only lines that have some number of words from a hulq wordlist, or, pass words through an English wordlist and don't change them if so (this might be very slow)[^slowwordlist]
[^slowwordlist]: (done -- it's not so slow)

- [ ] visible/editable word list pairs possibly extensible to other orthographies/languages
- [x] choose target font in dropdown[^choosefont]
[^choosefont]: but the font solution is not good

- [ ] check if first characters in line are LH for raw text editing