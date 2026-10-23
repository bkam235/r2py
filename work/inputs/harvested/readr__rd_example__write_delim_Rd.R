# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: write_delim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 15

suppressPackageStartupMessages(library(readr))
.old_wd <- setwd(tempdir())

# If only a file name is specified, write_()* will write
# the file to the current working directory.
write_csv(mtcars, "mtcars.csv")
write_tsv(mtcars, "mtcars.tsv")

# If you add an extension to the file name, write_()* will
# automatically compress the output.
write_tsv(mtcars, "mtcars.tsv.gz")
write_tsv(mtcars, "mtcars.tsv.bz2")
write_tsv(mtcars, "mtcars.tsv.xz")

setwd(.old_wd)