# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: print.ggplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 13

suppressPackageStartupMessages(library(ggplot2))
colours <- c("class", "drv", "fl")

# Doesn't seem to do anything!
for (colour in colours) {
  ggplot(mpg, aes(displ, hwy, colour = .data[[colour]])) +
    geom_point()
}

for (colour in colours) {
  print(ggplot(mpg, aes(displ, hwy, colour = .data[[colour]])) +
          geom_point())
}