# r2py crawler metadata
# package: mime
# source_type: rd_example
# topic: mimemap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mime\help
# lines: 6

suppressPackageStartupMessages(library(mime))
str(as.list(mimemap))
mimemap["pdf"]
mimemap[c("html", "js", "css")]
# additional MIME types (not exported)
mime:::mimeextra