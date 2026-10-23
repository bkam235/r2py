# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi-styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 34

suppressPackageStartupMessages(library(cli))
col_blue("Hello ", "world!")
cat(col_blue("Hello ", "world!"))

cat("... to highlight the", col_red("search term"),
    "in a block of text\n")

## Style stack properly
cat(col_green(
 "I am a green line ",
 col_blue(style_underline(style_bold("with a blue substring"))),
 " that becomes green again!"
))

error <- combine_ansi_styles("red", "bold")
warn <- combine_ansi_styles("magenta", "underline")
note <- col_cyan
cat(error("Error: subscript out of bounds!\n"))
cat(warn("Warning: shorter argument was recycled.\n"))
cat(note("Note: no such directory.\n"))

# style_no_* functions, note that the color is not removed
style_italic(col_green(paste0(
  "italic before, ",
  style_no_italic("normal here, "),
  "italic after"
)))

# avoiding  color for substring
style_italic(col_red(paste(
  "red before",
  col_none("not red between"),
  "red after"
)))