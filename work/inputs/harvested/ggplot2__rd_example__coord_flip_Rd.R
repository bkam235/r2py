# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: coord_flip.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 30

suppressPackageStartupMessages(library(ggplot2))
# The preferred method of creating horizontal instead of vertical boxplots
ggplot(diamonds, aes(price, cut)) +
  geom_boxplot()

# Using `coord_flip()` to make the same plot
ggplot(diamonds, aes(cut, price)) +
  geom_boxplot() +
  coord_flip()

# With swapped aesthetics, the y-scale controls the left axis
ggplot(diamonds, aes(y = carat)) +
  geom_histogram() +
  scale_y_reverse()

# In `coord_flip()`, the x-scale controls the left axis
ggplot(diamonds, aes(carat)) +
  geom_histogram() +
  coord_flip() +
  scale_x_reverse()

# In line and area plots, swapped aesthetics require an explicit orientation
df <- data.frame(a = 1:5, b = (1:5) ^ 2)
ggplot(df, aes(b, a)) +
  geom_area(orientation = "y")

# The same plot with `coord_flip()`
ggplot(df, aes(a, b)) +
  geom_area() +
  coord_flip()