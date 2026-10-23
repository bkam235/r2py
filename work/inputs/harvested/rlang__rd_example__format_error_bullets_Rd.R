# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: format_error_bullets.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 15

suppressPackageStartupMessages(library(rlang))
# All bullets
writeLines(format_error_bullets(c("foo", "bar")))

# This is equivalent to
writeLines(format_error_bullets(set_names(c("foo", "bar"), "*")))

# Supply named elements to format info, cross, and tick bullets
writeLines(format_error_bullets(c(i = "foo", x = "bar", v = "baz", "*" = "quux")))

# An unnamed element breaks the line
writeLines(format_error_bullets(c(i = "foo\nbar")))

# A " " element breaks the line within a bullet (with indentation)
writeLines(format_error_bullets(c(i = "foo", " " = "bar")))