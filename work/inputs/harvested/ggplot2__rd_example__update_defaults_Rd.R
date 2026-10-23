# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: update_defaults.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 28

suppressPackageStartupMessages(library(ggplot2))
# updating a geom's default aesthetic settings
# example: change geom_point()'s default color
GeomPoint$default_aes
update_geom_defaults("point", aes(color = "red"))
GeomPoint$default_aes
ggplot(mtcars, aes(mpg, wt)) + geom_point()

# reset single default
update_geom_defaults("point", NULL)

# reset all defaults
reset_geom_defaults()

# updating a stat's default aesthetic settings
# example: change stat_bin()'s default y-axis to the density scale
StatBin$default_aes
update_stat_defaults("bin", aes(y = after_stat(density)))
StatBin$default_aes
ggplot(data.frame(x = rnorm(1e3)), aes(x)) +
  geom_histogram() +
  geom_function(fun = dnorm, color = "red")

# reset single default
update_stat_defaults("bin", NULL)

# reset all defaults
reset_stat_defaults()