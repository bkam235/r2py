# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: hash_emoji.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 8

suppressPackageStartupMessages(library(cli))
hash_emoji(c("foo", NA, "bar", ""))$text

# if you increase `size`, the shorter hash is a prefix of the longer:
hash_emoji("foobar", 1)$text
hash_emoji("foobar", 2)$text
hash_emoji("foobar", 3)$text
hash_emoji("foobar", 4)$text