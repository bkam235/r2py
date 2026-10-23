# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: fcase.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 45

suppressPackageStartupMessages(library(data.table))
x = 1:10
fcase(
	x < 5L, 1L,
	x > 5L, 3L
)

fcase(
	x < 5L, 1L:10L,
	x > 5L, 3L:12L
)

# Lazy evaluation example
fcase(
	x < 5L, 1L,
	x >= 5L, 3L,
	x == 5L, stop("provided value is an unexpected one!")
)

# fcase preserves attributes, example with dates
fcase(
	x < 5L, as.Date("2019-10-11"),
	x > 5L, as.Date("2019-10-14")
)

# fcase example with factor; note the matching levels
fcase(
	x < 5L, factor("a", levels=letters[1:3]),
	x > 5L, factor("b", levels=letters[1:3])
)

# Example of using the 'default' argument
fcase(
	x < 5L, 1L,
	x > 5L, 3L,
	default = 5L
)

# fcase can be used for recursion, unlike fifelse
# Recursive function to calculate the Greatest Common Divisor
gcd_dt = function(x,y) {
  r = x%%y
  fcase(!r, y, r, gcd_dt(x, y)) # Recursive call must be in the last when-value pair
}
gcd_dt(10L, 1L)