# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_reorder.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 27

suppressPackageStartupMessages(library(forcats))
# fct_reorder() -------------------------------------------------------------
# Useful when a categorical variable is mapped to position
boxplot(Sepal.Width ~ Species, data = iris)
boxplot(Sepal.Width ~ fct_reorder(Species, Sepal.Width), data = iris)

# or with
library(ggplot2)
ggplot(iris, aes(fct_reorder(Species, Sepal.Width), Sepal.Width)) +
  geom_boxplot()

# fct_reorder2() -------------------------------------------------------------
# Useful when a categorical variable is mapped to color, size, shape etc

chks <- subset(ChickWeight, as.integer(Chick) < 10)
chks <- transform(chks, Chick = fct_shuffle(Chick))

# Without reordering it's hard to match line to legend
ggplot(chks, aes(Time, weight, colour = Chick)) +
  geom_point() +
  geom_line()

# With reordering it's much easier
ggplot(chks, aes(Time, weight, colour = fct_reorder2(Chick, Time, weight))) +
  geom_point() +
  geom_line() +
  labs(colour = "Chick")