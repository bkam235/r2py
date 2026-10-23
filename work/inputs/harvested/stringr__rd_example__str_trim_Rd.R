# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_trim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 6

suppressPackageStartupMessages(library(stringr))
str_trim("  String with trailing and leading white space\t")
str_trim("\n\nString with trailing and leading white space\n\n")

str_squish("  String with trailing,  middle, and leading white space\t")
str_squish("\n\nString with excess,  trailing and leading white   space\n\n")