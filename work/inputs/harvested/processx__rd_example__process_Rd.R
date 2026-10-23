# r2py crawler metadata
# package: processx
# source_type: rd_example
# topic: process.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\processx\help
# lines: 13

suppressPackageStartupMessages(library(processx))
if (identical(Sys.getenv("IN_PKGDOWN"), "true")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
p <- process$new("sleep", "2")
p$is_alive()
p
p$kill()
p$is_alive()

p <- process$new("sleep", "1")
p$is_alive()
Sys.sleep(2)
p$is_alive()
}) # examplesIf