# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_replace.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 40

suppressPackageStartupMessages(library(stringi))
stri_replace_all_charclass('aaaa', '[a]', 'b', merge=c(TRUE, FALSE))

stri_replace_all_charclass('a\nb\tc   d', '\\p{WHITE_SPACE}', ' ')
stri_replace_all_charclass('a\nb\tc   d', '\\p{WHITE_SPACE}', ' ', merge=TRUE)

s <- 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'
stri_replace_all_fixed(s, ' ', '#')
stri_replace_all_fixed(s, 'o', '0')

stri_replace_all_fixed(c('1', 'NULL', '3'), 'NULL', NA)

stri_replace_all_regex(s, ' .*? ', '#')
stri_replace_all_regex(s, '(el|s)it', '1234')
stri_replace_all_regex('abaca', 'a', c('!', '*'))
stri_replace_all_regex('123|456|789', '(\\p{N}).(\\p{N})', '$2-$1')
stri_replace_all_regex(c('stringi R', 'REXAMINE', '123'), '( R|R.)', ' r ')

# named capture groups are available since ICU 55

stri_replace_all_regex('words 123 and numbers 456',
   '(?<numbers>[0-9]+)', '!${numbers}!')


# Compare the results:
stri_replace_all_fixed('The quick brown fox jumped over the lazy dog.',
     c('quick', 'brown', 'fox'), c('slow',  'black', 'bear'), vectorize_all=TRUE)
stri_replace_all_fixed('The quick brown fox jumped over the lazy dog.',
     c('quick', 'brown', 'fox'), c('slow',  'black', 'bear'), vectorize_all=FALSE)

# Compare the results:
stri_replace_all_fixed('The quicker brown fox jumped over the lazy dog.',
     c('quick', 'brown', 'fox'), c('slow',  'black', 'bear'), vectorize_all=FALSE)
stri_replace_all_regex('The quicker brown fox jumped over the lazy dog.',
     '\\b'%s+%c('quick', 'brown', 'fox')%s+%'\\b', c('slow',  'black', 'bear'), vectorize_all=FALSE)

# Searching for the last occurrence:
# Note the difference - regex searches left to right, with no overlaps.
stri_replace_last_fixed("agAGA", "aga", "*", case_insensitive=TRUE)
stri_replace_last_regex("agAGA", "aga", "*", case_insensitive=TRUE)