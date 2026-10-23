# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: crayon.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 20

suppressPackageStartupMessages(library(crayon))
cat(blue("Hello", "world!"))

cat("... to highlight the " %+% red("search term") %+%
    " in a block of text")

cat(yellow$bgMagenta$bold('Hello world!'))

cat(green(
 'I am a green line ' %+%
 blue$underline$bold('with a blue substring') %+%
 ' that becomes green again!'
))

error <- red $ bold
warn <- magenta $ underline
note <- cyan
cat(error("Error: subscript out of bounds!\n"))
cat(warn("Warning: shorter argument was recycled.\n"))
cat(note("Note: no such directory.\n"))