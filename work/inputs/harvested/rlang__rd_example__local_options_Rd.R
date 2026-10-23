# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: local_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 20

suppressPackageStartupMessages(library(rlang))
# Store and retrieve a global option:
push_options(my_option = 10)
peek_option("my_option")

# Change the option temporarily:
with_options(my_option = 100, peek_option("my_option"))
peek_option("my_option")

# The scoped variant is useful within functions:
fn <- function() {
  local_options(my_option = 100)
  peek_option("my_option")
}
fn()
peek_option("my_option")

# The plural peek returns a named list:
peek_options("my_option")
peek_options("my_option", "digits")