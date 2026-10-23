# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: element.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 37

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
plot <- ggplot(mpg, aes(displ, hwy)) + geom_point()

# Turning off theme elements by setting them to blank
plot + theme(
  panel.background = element_blank(),
  axis.text = element_blank()
)

# Text adjustments
plot + theme(
  axis.text = element_text(colour = "red", size = rel(1.5))
)

# Turning on the axis line with an arrow
plot + theme(
  axis.line = element_line(arrow = arrow())
)

plot + theme(
  panel.background = element_rect(fill = "white"),
  plot.margin = margin_auto(2, unit = "cm"),
  plot.background = element_rect(
    fill = "grey90",
    colour = "black",
    linewidth = 1
  )
)

ggplot(mpg, aes(displ, hwy)) +
  geom_point() +
  geom_smooth(formula = y ~ x, method = "lm") +
  theme(geom = element_geom(
    ink = "red", accent = "black",
    pointsize = 1, linewidth = 2
  ))