# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: make_constructor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 34

suppressPackageStartupMessages(library(ggplot2))
# For testing purposes, a geom that returns grobs
GeomTest <- ggproto(
  "GeomTest", Geom,
  draw_group = function(..., grob = grid::pointsGrob()) {
    return(grob)
  }
)
# Creating a constructor
geom_test <- make_constructor(GeomTest)

# Note that `grob` is automatically an argument to the function
names(formals(geom_test))

# Use in a plot
set.seed(1234)
p <- ggplot(mtcars, aes(disp, mpg))
p + geom_test()
p + geom_test(grob = grid::circleGrob())

# The `checks` argument can be used to evaluate arbitrary expressions in
# the constructor before building the layer.
geom_path2 <- make_constructor(
  GeomPath, checks = rlang::exprs(
    match.arg(lineend, c("butt", "round", "square")),
    match.arg(linejoin, c("round", "mitre", "bevel"))
  )
)

# Note the inclusion of the expressions
print(geom_path2)

# Argument mismatch is detected
try(geom_path2(linejoin = "foo"))