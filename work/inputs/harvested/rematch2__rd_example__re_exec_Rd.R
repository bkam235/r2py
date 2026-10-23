# r2py crawler metadata
# package: rematch2
# source_type: rd_example
# topic: re_exec.Rd
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
# Match first occurrence
pos <- re_exec(notables, name_rex)
pos

# Custom $ to extract matches and positions
pos$first$match
pos$first$start
pos$first$end