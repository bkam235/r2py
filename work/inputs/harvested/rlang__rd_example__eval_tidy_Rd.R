# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: eval_tidy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 28

suppressPackageStartupMessages(library(rlang))
# With simple defused expressions eval_tidy() works the same way as
# eval():
fruit <- "apple"
vegetable <- "potato"
expr <- quote(paste(fruit, vegetable, sep = " or "))
expr

eval(expr)
eval_tidy(expr)

# Both accept a data mask as argument:
data <- list(fruit = "banana", vegetable = "carrot")
eval(expr, data)
eval_tidy(expr, data)

# The main difference is that eval_tidy() supports quosures:
with_data <- function(data, expr) {
  quo <- enquo(expr)
  eval_tidy(quo, data)
}
with_data(NULL, fruit)
with_data(data, fruit)

# eval_tidy() installs the `.data` and `.env` pronouns to allow
# users to be explicit about variable references:
with_data(data, .data$fruit)
with_data(data, .env$fruit)