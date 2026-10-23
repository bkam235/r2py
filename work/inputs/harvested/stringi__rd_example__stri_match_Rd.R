# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 25

suppressPackageStartupMessages(library(stringi))
stri_match_all_regex('breakfast=eggs, lunch=pizza, dessert=icecream',
   '(\\w+)=(\\w+)')
stri_match_all_regex(c('breakfast=eggs', 'lunch=pizza', 'no food here'),
   '(\\w+)=(\\w+)')
stri_match_all_regex(c('breakfast=eggs;lunch=pizza',
   'breakfast=bacon;lunch=spaghetti', 'no food here'),
   '(\\w+)=(\\w+)')
stri_match_all_regex(c('breakfast=eggs;lunch=pizza',
   'breakfast=bacon;lunch=spaghetti', 'no food here'),
   '(?<when>\\w+)=(?<what>\\w+)')  # named capture groups
stri_match_first_regex(c('breakfast=eggs;lunch=pizza',
   'breakfast=bacon;lunch=spaghetti', 'no food here'),
   '(\\w+)=(\\w+)')
stri_match_last_regex(c('breakfast=eggs;lunch=pizza',
   'breakfast=bacon;lunch=spaghetti', 'no food here'),
   '(\\w+)=(\\w+)')

stri_match_first_regex(c('abcd', ':abcd', ':abcd:'), '^(:)?([^:]*)(:)?$')
stri_match_first_regex(c('abcd', ':abcd', ':abcd:'), '^(:)?([^:]*)(:)?$', cg_missing='')

# Match all the pattern of the form XYX, including overlapping matches:
stri_match_all_regex('ACAGAGACTTTAGATAGAGAAGA', '(?=(([ACGT])[ACGT]\\2))')[[1]][,2]
# Compare the above to:
stri_extract_all_regex('ACAGAGACTTTAGATAGAGAAGA', '([ACGT])[ACGT]\\1')