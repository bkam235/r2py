# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: read_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
# two files in this package
fs = system.file("scripts", c("call-fun.R", "child-pids.sh"), package = "xfun")
xfun::read_all(fs)

# add file paths before file content and an empty line after content
xfun::read_all(fs, before = function(f) paste("#-----", f, "-----"), after = "")

# add constants
xfun::read_all(fs, before = "/*", after = c("*/", ""))