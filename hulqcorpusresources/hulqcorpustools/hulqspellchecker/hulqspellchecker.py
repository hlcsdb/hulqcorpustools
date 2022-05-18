from spellchecker import SpellChecker

spell = SpellChecker()

misspelled = spell.unknown(['something', 'is', 'hapenning', 'here'])

for word in misspelled:
    print(spell.correction(word))

    print(spell.candidates(word))