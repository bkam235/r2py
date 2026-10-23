# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: mime_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 7

suppressPackageStartupMessages(library(xfun))
if (tolower(Sys.getenv('CI')) == 'true') {
f = list.files(R.home("doc"), full.names = TRUE)
mime_type(f)
mime_type(f, FALSE)  # don't use mime
mime_type(f, FALSE, NA)  # run command for files without extension
}