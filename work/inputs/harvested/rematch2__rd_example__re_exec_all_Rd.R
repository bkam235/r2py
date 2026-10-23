# r2py crawler metadata
# package: rematch2
# source_type: rd_example
# topic: re_exec_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rematch2\help
# lines: 17

suppressPackageStartupMessages(library(rematch2))
name_rex <- paste0(
  "(?<first>[[:upper:]][[:lower:]]+) ",
  "(?<last>[[:upper:]][[:lower:]]+)"
)
notables <- c(
  "  Ben Franklin and Jefferson Davis",
  "\tMillard Fillmore"
)
# All occurrences
allpos <- re_exec_all(notables, name_rex)
allpos

# Custom $ to extract matches and positions
allpos$first$match
allpos$first$start
allpos$first$end