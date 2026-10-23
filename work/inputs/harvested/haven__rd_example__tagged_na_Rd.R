# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: tagged_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 19

suppressPackageStartupMessages(library(haven))
x <- c(1:5, tagged_na("a"), tagged_na("z"), NA)

# Tagged NA's work identically to regular NAs
x
is.na(x)

# To see that they're special, you need to use na_tag(),
# is_tagged_na(), or print_tagged_na():
is_tagged_na(x)
na_tag(x)
print_tagged_na(x)

# You can test for specific tagged NAs with the second argument
is_tagged_na(x, "a")

# Because the support for tagged's NAs is somewhat tagged on to R,
# the left-most NA will tend to be preserved in arithmetic operations.
na_tag(tagged_na("a") + tagged_na("z"))