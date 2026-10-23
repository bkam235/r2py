# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: subtheme.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 23

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(mtcars, aes(disp, mpg, colour = drat)) +
  geom_point()

red_text <- element_text(colour = "red")
red_line <- element_line(colour = "red")

# The theme settings below:
p + theme(
  axis.title.x.bottom = red_text,
  axis.text.x.bottom  = red_text,
  axis.line.x.bottom  = red_line,
  axis.ticks.x.bottom = red_line
)

# Are equivalent to these less verbose theme settings
p + theme_sub_axis_bottom(
  title = red_text,
  text  = red_text,
  line  = red_line,
  ticks = red_line
)