# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: locales_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\locales.R
# lines: 26

suppressPackageStartupMessages(library(readr))
library(stringi)
x <- "Émigré cause célèbre déjà vu.\n"
y <- stri_conv(x, "UTF-8", "latin1")

# These strings look like they're identical:
x
y
identical(x, y)

# But they have different encodings:
Encoding(x)
Encoding(y)

# That means while they print the same, their raw (binary)
# representation is actually quite different:
charToRaw(x)
charToRaw(y)

# readr expects strings to be encoded as UTF-8. If they're
# not, you'll get weird characters
parse_character(x)
parse_character(y)

# If you know the encoding, supply it:
parse_character(y, locale = locale(encoding = "latin1"))