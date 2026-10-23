# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: locales_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\locales.R
# lines: 7

suppressPackageStartupMessages(library(readr))
maori <- locale(date_names(
  day = c("Rātapu", "Rāhina", "Rātū", "Rāapa", "Rāpare", "Rāmere", "Rāhoroi"),
  mon = c("Kohi-tātea", "Hui-tanguru", "Poutū-te-rangi", "Paenga-whāwhā",
    "Haratua", "Pipiri", "Hōngongoi", "Here-turi-kōkā", "Mahuru",
    "Whiringa-ā-nuku", "Whiringa-ā-rangi", "Hakihea")
))