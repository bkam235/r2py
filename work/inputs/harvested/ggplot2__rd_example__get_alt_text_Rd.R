# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: get_alt_text.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mpg, aes(displ, hwy)) +
  geom_point()

# Returns an empty string
get_alt_text(p)

# A user provided alt text
p <- p + labs(
  alt = paste("A scatterplot showing the negative correlation between engine",
              "displacement as a function of highway miles per gallon")
)

get_alt_text(p)