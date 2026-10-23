# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_function.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 48

suppressPackageStartupMessages(library(ggplot2))
# geom_function() is useful for overlaying functions
set.seed(1492)
ggplot(data.frame(x = rnorm(100)), aes(x)) +
  geom_density() +
  geom_function(fun = dnorm, colour = "red")

# To plot functions without data, specify range of x-axis
base <-
  ggplot() +
  xlim(-5, 5)

base + geom_function(fun = dnorm)

base + geom_function(fun = dnorm, args = list(mean = 2, sd = .5))

# The underlying mechanics evaluate the function at discrete points
# and connect the points with lines
base + stat_function(fun = dnorm, geom = "point")

base + stat_function(fun = dnorm, geom = "point", n = 20)

base + stat_function(fun = dnorm, geom = "polygon", color = "blue", fill = "blue", alpha = 0.5)

base + geom_function(fun = dnorm, n = 20)

# Two functions on the same plot
base +
  geom_function(aes(colour = "normal"), fun = dnorm) +
  geom_function(aes(colour = "t, df = 1"), fun = dt, args = list(df = 1))

# Using a custom anonymous function
base + geom_function(fun = \(x) 0.5 * exp(-abs(x)))
# or using lambda syntax:
# base + geom_function(fun = ~ 0.5 * exp(-abs(.x)))
# or using a custom named function:
# f <- function(x) 0.5 * exp(-abs(x))
# base + geom_function(fun = f)

# Using xlim to restrict the range of function
ggplot(data.frame(x = rnorm(100)), aes(x)) +
geom_density() +
geom_function(fun = dnorm, colour = "red", xlim=c(-1, 1))

# Using xlim to widen the range of function
ggplot(data.frame(x = rnorm(100)), aes(x)) +
geom_density() +
geom_function(fun = dnorm, colour = "red", xlim=c(-7, 7))