# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: coord_radial.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 62

suppressPackageStartupMessages(library(ggplot2))
# NOTE: Use these plots with caution - polar coordinates has
# major perceptual problems.  The main point of these examples is
# to demonstrate how these common plots can be described in the
# grammar.  Use with EXTREME caution.

# A pie chart = stacked bar chart + polar coordinates
pie <- ggplot(mtcars, aes(x = factor(1), fill = factor(cyl))) +
 geom_bar(width = 1)
pie + coord_radial(theta = "y", expand = FALSE)



# A coxcomb plot = bar chart + polar coordinates
cxc <- ggplot(mtcars, aes(x = factor(cyl))) +
  geom_bar(width = 1, colour = "black")
cxc + coord_radial(expand = FALSE)
# A new type of plot?
cxc + coord_radial(theta = "y", expand = FALSE)

# The bullseye chart
pie + coord_radial(expand = FALSE)

# Hadley's favourite pie chart
df <- data.frame(
  variable = c("does not resemble", "resembles"),
  value = c(20, 80)
)
ggplot(df, aes(x = "", y = value, fill = variable)) +
  geom_col(width = 1) +
  scale_fill_manual(values = c("red", "yellow")) +
  coord_radial("y", start = pi / 3, expand =  FALSE) +
  labs(title = "Pac man")

# Windrose + doughnut plot
if (require("ggplot2movies")) {
movies$rrating <- cut_interval(movies$rating, length = 1)
movies$budgetq <- cut_number(movies$budget, 4)

doh <- ggplot(movies, aes(x = rrating, fill = budgetq))

# Wind rose
doh + geom_bar(width = 1) + coord_radial(expand = FALSE)
# Race track plot
doh + geom_bar(width = 0.9, position = "fill") +
  coord_radial(theta = "y", expand = FALSE)
}

# A partial polar plot
ggplot(mtcars, aes(disp, mpg)) +
  geom_point() +
  coord_radial(start = -0.4 * pi, end = 0.4 * pi, inner.radius = 0.3)

# Similar with coord_cartesian(), you can set limits.
ggplot(mtcars, aes(disp, mpg)) +
  geom_point() +
  coord_radial(
    start = -0.4 * pi,
    end = 0.4 * pi, inner.radius = 0.3,
    thetalim = c(200, 300),
    rlim = c(15, 30),
  )