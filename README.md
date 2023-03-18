# hulqcorpustools
Some useful tools to be used in processing Hul’q’umi’num’ texts.

# NOTE ON USE
Right now, since everything is still under development and I (Zack) am still trying to get everything working under best practices, including modularizing everything to share resources needed by multiple functions, you can't really use any script directly. However, if you clone this repo and write scripts in another place (for example, currently I have them in /hulqcorpustools/tests/, not to be confused with the source dir /hulqcorpustools/hulqcorpustools/) and import things from the package that way, everything should work fine. Except for bugs, of course.

## hulqtransliterator
Transliterate one of the various ways of writing Hul’q’umi’num’ into another.

### NEW FEATURES TO IMPLEMENT:
#### REAL FEATURES:
- [ ] get the standalone executable to work ([py2app](https://github.com/ronaldoussoren/py2app) please.... (I think this was actually my fault - Z))
- [ ] drag and drop file onto executable instead of using the file browser
- [ ] working command-line interface instead of failed GUI or pointing at batch file folders

#### NEW FEATURES?!:
- [x] instant transliterator that transliterates on keypress
    - [x] use same engine as file transliterator
- [x] replace only lines that have some number of words from a hulq wordlist, or, pass words through an English wordlist and don't change them if so (this might be very slow)[^slowwordlist]
[^slowwordlist]: (done -- it's not so slow)

- [ ] visible/editable word list pairs possibly extensible to other orthographies/languages
- [x] choose target font in dropdown[^choosefont]
[^choosefont]: but the font solution is not good

- [ ] check if first characters in line are LH\t for plain text editing of files