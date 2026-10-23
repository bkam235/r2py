# r2py crawler metadata
# package: jsonlite
# source_type: vignette
# topic: json-aaquickstart_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\doc\json-aaquickstart.R
# lines: 9

suppressPackageStartupMessages(library(jsonlite))
library(knitr)
opts_chunk$set(comment="")

#this replaces tabs by spaces because latex-verbatim doesn't like tabs
#no longer needed because yajl does not use tabs.
#toJSON <- function(...){
#  gsub("\t", "  ", jsonlite::toJSON(...), fixed=TRUE);
#}