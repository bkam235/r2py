# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_colour_discrete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(mpg, aes(displ, hwy, colour = class)) +
  geom_point()

# You can use the scale to give a palette directly
p + scale_colour_discrete(palette = scales::pal_brewer(palette = "Dark2"))

# The default colours are encoded into the theme
p + theme(palette.colour.discrete = scales::pal_grey())

# You can globally set default colour palette via the theme
old <- update_theme(palette.colour.discrete = scales::pal_viridis())

# Plot now shows new global default
p

# Restoring the previous theme
theme_set(old)