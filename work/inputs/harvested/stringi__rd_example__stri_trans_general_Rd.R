# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_trans_general.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 26

suppressPackageStartupMessages(library(stringi))
stri_trans_general('gro\u00df', 'latin-ascii')
stri_trans_general('stringi', 'latin-greek')
stri_trans_general('stringi', 'latin-cyrillic')
stri_trans_general('stringi', 'upper') # see stri_trans_toupper
stri_trans_general('\u0104', 'nfd; lower') # compound id; see stri_trans_nfd
stri_trans_general('Marek G\u0105golewski', 'pl-pl_FONIPA')
stri_trans_general('\u2620', 'any-name') # character name
stri_trans_general('\\N{latin small letter a}', 'name-any') # decode name
stri_trans_general('\u2620', 'hex/c') # to hex
stri_trans_general("\u201C\u2026\u201D \u0105\u015B\u0107\u017C",
    "NFKD; NFC; [^\\p{L}] latin-ascii")

x <- "\uC885\uB85C\uAD6C \uC0AC\uC9C1\uB3D9"
stringi::stri_trans_general(x, "Hangul-Latin")
# Deviate from the ICU rules of romanisation of Korean,
# see https://en.wikipedia.org/wiki/Romanization_of_Korean
id <- "
    :: NFD;
    \u11A8 > k;
    \u11AE > t;
    \u11B8 > p;
    \u1105 > r;
    :: Hangul-Latin;
"
stringi::stri_trans_general(x, id, rules=TRUE)