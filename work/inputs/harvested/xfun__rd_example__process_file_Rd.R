# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: process_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 6

suppressPackageStartupMessages(library(xfun))
f = tempfile()
xfun::write_utf8("Hello World", f)
xfun::process_file(f, function(x) gsub("World", "woRld", x))
xfun::read_utf8(f)  # see if it has been updated
file.remove(f)