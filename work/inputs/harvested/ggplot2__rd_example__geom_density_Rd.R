# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_density.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 40

suppressPackageStartupMessages(library(ggplot2))
ggplot(diamonds, aes(carat)) +
  geom_density()
# Map the values to y to flip the orientation
ggplot(diamonds, aes(y = carat)) +
  geom_density()

ggplot(diamonds, aes(carat)) +
  geom_density(adjust = 1/5)
ggplot(diamonds, aes(carat)) +
  geom_density(adjust = 5)

ggplot(diamonds, aes(depth, colour = cut)) +
  geom_density() +
  xlim(55, 70)
ggplot(diamonds, aes(depth, fill = cut, colour = cut)) +
  geom_density(alpha = 0.1) +
  xlim(55, 70)

# Use `bounds` to adjust computation for known data limits
big_diamonds <- diamonds[diamonds$carat >= 1, ]
ggplot(big_diamonds, aes(carat)) +
  geom_density(color = 'red') +
  geom_density(bounds = c(1, Inf), color = 'blue')


# Stacked density plots: if you want to create a stacked density plot, you
# probably want to 'count' (density * n) variable instead of the default
# density

# Loses marginal densities
ggplot(diamonds, aes(carat, fill = cut)) +
  geom_density(position = "stack")
# Preserves marginal densities
ggplot(diamonds, aes(carat, after_stat(count), fill = cut)) +
  geom_density(position = "stack")

# You can use position="fill" to produce a conditional density estimate
ggplot(diamonds, aes(carat, after_stat(count), fill = cut)) +
  geom_density(position = "fill")