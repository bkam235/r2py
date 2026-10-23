# r2py crawler metadata
# package: ini
# source_type: rd_example
# topic: read.ini.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ini\help
# lines: 18

suppressPackageStartupMessages(library(ini))
## Create a new temp ini for reading
iniFile <- tempfile(fileext = '.ini')

sink(iniFile)
cat("; This line is a comment\n")
cat("# This one too!\n")
cat("[    Hello World]\n")
cat("Foo = Bar          \n")
cat("Foo1 = Bar=345 \n")
sink()

## Read ini
checkini <- read.ini(iniFile)

## Check structure
checkini
checkini$`Hello World`$Foo