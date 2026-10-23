# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: spruce-multiple.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 17

suppressPackageStartupMessages(library(hardhat))
spruce_numeric_multiple(1:3, foo = 2:4)

spruce_class_multiple(
  one_step = factor(c("a", "b", "c")),
  two_step = factor(c("a", "c", "c"))
)

one_step <- matrix(c(.3, .7, .0, .1, .3, .6), nrow = 2, byrow = TRUE)
two_step <- matrix(c(.2, .7, .1, .2, .4, .4), nrow = 2, byrow = TRUE)
binary <- matrix(c(.5, .5, .4, .6), nrow = 2, byrow = TRUE)

spruce_prob_multiple(
  one_step = spruce_prob(c("a", "b", "c"), one_step),
  two_step = spruce_prob(c("a", "b", "c"), two_step),
  binary = spruce_prob(c("yes", "no"), binary)
)