# r2py crawler metadata
# package: blob
# source_type: rd_example
# topic: blob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\blob\help
# lines: 8

suppressPackageStartupMessages(library(blob))
x1 <- charToRaw("Good morning")
x2 <- as.raw(c(0x48, 0x65, 0x6c, 0x6c, 0x6f))

new_blob(list(x1, x2))
blob(x1, x2)

as.blob(c("Good morning", "Good evening"))