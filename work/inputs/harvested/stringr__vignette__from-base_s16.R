# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 10

suppressPackageStartupMessages(library(stringr))
head(sentences)
noun <- "([A]a|[Tt]he) ([^ ]+)"

# base
matches <- regexec(pattern = noun, text = head(sentences))
do.call("rbind", regmatches(x = head(sentences), m = matches))

# stringr
str_match(head(sentences), pattern = noun)