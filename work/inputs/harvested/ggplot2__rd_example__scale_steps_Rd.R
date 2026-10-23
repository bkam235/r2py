# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_steps.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 22

suppressPackageStartupMessages(library(ggplot2))
set.seed(1)
df <- data.frame(
  x = runif(100),
  y = runif(100),
  z1 = rnorm(100)
)

# Use scale_colour_steps for a standard binned gradient
ggplot(df, aes(x, y)) +
  geom_point(aes(colour = z1)) +
  scale_colour_steps()

# Get a divergent binned scale with the *2 variant
ggplot(df, aes(x, y)) +
  geom_point(aes(colour = z1)) +
  scale_colour_steps2()

# Define your own colour ramp to extract binned colours from
ggplot(df, aes(x, y)) +
  geom_point(aes(colour = z1)) +
  scale_colour_stepsn(colours = terrain.colors(10))