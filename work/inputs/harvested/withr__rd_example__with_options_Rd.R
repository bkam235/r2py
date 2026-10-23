# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 26

suppressPackageStartupMessages(library(withr))
# number of significant digits to print
getOption("digits")
# modify temporarily the number of significant digits to print
with_options(list(digits = 3), getOption("digits"))
with_options(list(digits = 3), print(pi))

# modify temporarily the character to be used as the decimal point
getOption("digits")
with_options(list(OutDec = ","), print(pi))

# modify temporarily multiple options
with_options(list(OutDec = ",", digits = 3), print(pi))

# modify, within the scope of the function, the number of
# significant digits to print
print_3_digits <- function(x) {
  # assign 3 to the option "digits" for the rest of this function
  # after the function exits, the option will return to its previous
  # value
  local_options(list(digits = 3))
  print(x)
}

print_3_digits(pi)  # returns 3.14
print(pi)           # returns 3.141593