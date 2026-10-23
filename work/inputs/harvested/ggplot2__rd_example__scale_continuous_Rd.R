# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_continuous.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 53

suppressPackageStartupMessages(library(ggplot2))
p1 <- ggplot(mpg, aes(displ, hwy)) +
  geom_point()
p1

# Manipulating the default position scales lets you:
#  * change the axis labels
p1 +
  scale_x_continuous("Engine displacement (L)") +
  scale_y_continuous("Highway MPG")

# You can also use the short-cut labs().
# Use NULL to suppress axis labels
p1 + labs(x = NULL, y = NULL)

#  * modify the axis limits
p1 + scale_x_continuous(limits = c(2, 6))
p1 + scale_x_continuous(limits = c(0, 10))

# you can also use the short hand functions `xlim()` and `ylim()`
p1 + xlim(2, 6)

#  * choose where the ticks appear
p1 + scale_x_continuous(breaks = c(2, 4, 6))

#  * choose your own labels
p1 + scale_x_continuous(
  breaks = c(2, 4, 6),
  label = c("two", "four", "six")
)

# Typically you'll pass a function to the `labels` argument.
# Some common formats are built into the scales package:
set.seed(1)
df <- data.frame(
  x = rnorm(10) * 100000,
  y = seq(0, 1, length.out = 10)
)
p2 <- ggplot(df, aes(x, y)) + geom_point()
p2 + scale_y_continuous(labels = scales::label_percent())
p2 + scale_y_continuous(labels = scales::label_dollar())
p2 + scale_x_continuous(labels = scales::label_comma())

# You can also override the default linear mapping by using a
# transformation. There are three shortcuts:
p1 + scale_y_log10()
p1 + scale_y_sqrt()
p1 + scale_y_reverse()

# Or you can supply a transformation in the `trans` argument:
p1 + scale_y_continuous(transform = scales::transform_reciprocal())

# You can also create your own. See ?scales::new_transform