# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: dplyr-locale.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 23

suppressPackageStartupMessages(library(dplyr))
if (dplyr:::has_minimum_stringi()) withAutoprint({ # examplesIf
df <- tibble(x = c("a", "b", "C", "B", "c"))
df

# Default locale is C, which groups the English alphabet by case, placing
# uppercase letters before lowercase letters.
arrange(df, x)

# The American English locale groups the alphabet by letter.
# Explicitly override `.locale` with `"en"` for this ordering.
arrange(df, x, .locale = "en")

# This Danish letter is expected to sort after `z`
df <- tibble(x = c("o", "p", "\u00F8", "z"))
df

# The American English locale sorts it right after `o`
arrange(df, x, .locale = "en")

# Using `"da"` for Danish ordering gives the expected result
arrange(df, x, .locale = "da")
}) # examplesIf