# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_detect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 19

suppressPackageStartupMessages(library(stringi))
stri_detect_fixed(c('stringi R', 'R STRINGI', '123'), c('i', 'R', '0'))
stri_detect_fixed(c('stringi R', 'R STRINGI', '123'), 'R')

stri_detect_charclass(c('stRRRingi','R STRINGI', '123'),
   c('\\p{Ll}', '\\p{Lu}', '\\p{Zs}'))

stri_detect_regex(c('stringi R', 'R STRINGI', '123'), 'R.')
stri_detect_regex(c('stringi R', 'R STRINGI', '123'), '[[:alpha:]]*?')
stri_detect_regex(c('stringi R', 'R STRINGI', '123'), '[a-zC1]')
stri_detect_regex(c('stringi R', 'R STRINGI', '123'), '( R|RE)')
stri_detect_regex('stringi', 'STRING.', case_insensitive=TRUE)

stri_detect_regex(c('abc', 'def', '123', 'ghi', '456', '789', 'jkl'),
   '^[0-9]+$', max_count=1)
stri_detect_regex(c('abc', 'def', '123', 'ghi', '456', '789', 'jkl'),
   '^[0-9]+$', max_count=2)
stri_detect_regex(c('abc', 'def', '123', 'ghi', '456', '789', 'jkl'),
   '^[0-9]+$', negate=TRUE, max_count=3)