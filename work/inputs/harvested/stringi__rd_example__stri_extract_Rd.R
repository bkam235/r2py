# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_extract.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 34

suppressPackageStartupMessages(library(stringi))
stri_extract_all('XaaaaX', regex=c('\\p{Ll}', '\\p{Ll}+', '\\p{Ll}{2,3}', '\\p{Ll}{2,3}?'))
stri_extract_all('Bartolini', coll='i')
stri_extract_all('stringi is so good!', charclass='\\p{Zs}') # all white-spaces

stri_extract_all_charclass(c('AbcdeFgHijK', 'abc', 'ABC'), '\\p{Ll}')
stri_extract_all_charclass(c('AbcdeFgHijK', 'abc', 'ABC'), '\\p{Ll}', merge=FALSE)
stri_extract_first_charclass('AaBbCc', '\\p{Ll}')
stri_extract_last_charclass('AaBbCc', '\\p{Ll}')


# emoji support available since ICU 57
stri_extract_all_charclass(stri_enc_fromutf32(32:55200), '\\p{EMOJI}')


stri_extract_all_coll(c('AaaaaaaA', 'AAAA'), 'a')
stri_extract_first_coll(c('Yy\u00FD', 'AAA'), 'y', strength=2, locale='sk_SK')
stri_extract_last_coll(c('Yy\u00FD', 'AAA'), 'y',  strength=1, locale='sk_SK')

stri_extract_all_regex('XaaaaX', c('\\p{Ll}', '\\p{Ll}+', '\\p{Ll}{2,3}', '\\p{Ll}{2,3}?'))
stri_extract_first_regex('XaaaaX', c('\\p{Ll}', '\\p{Ll}+', '\\p{Ll}{2,3}', '\\p{Ll}{2,3}?'))
stri_extract_last_regex('XaaaaX', c('\\p{Ll}', '\\p{Ll}+', '\\p{Ll}{2,3}', '\\p{Ll}{2,3}?'))

stri_list2matrix(stri_extract_all_regex('XaaaaX', c('\\p{Ll}', '\\p{Ll}+')))
stri_extract_all_regex('XaaaaX', c('\\p{Ll}', '\\p{Ll}+'), simplify=TRUE)
stri_extract_all_regex('XaaaaX', c('\\p{Ll}', '\\p{Ll}+'), simplify=NA)

stri_extract_all_fixed('abaBAba', 'Aba', case_insensitive=TRUE)
stri_extract_all_fixed('abaBAba', 'Aba', case_insensitive=TRUE, overlap=TRUE)

# Searching for the last occurrence:
# Note the difference - regex searches left to right, with no overlaps.
stri_extract_last_fixed("agAGA", "aga", case_insensitive=TRUE)
stri_extract_last_regex("agAGA", "aga", case_insensitive=TRUE)