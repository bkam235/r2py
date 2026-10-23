# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_colour_continuous.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 23

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(mpg, aes(displ, hwy, colour = cty)) +
  geom_point()

# You can use the scale to give a palette directly
p + scale_colour_continuous(palette = c("#FEE0D2", "#FC9272", "#DE2D26"))

# The default colours are encoded into the theme
p + theme(palette.colour.continuous = c("#DEEBF7", "#9ECAE1", "#3182BD"))

# You can globally set default colour palette via the theme
old <- update_theme(palette.colour.continuous = c("#E5F5E0", "#A1D99B", "#31A354"))

# Plot now shows new global default
p

# The default binned colour scale uses the continuous palette
p + scale_colour_binned() +
  theme(palette.colour.continuous = c("#EFEDF5", "#BCBDDC", "#756BB1"))

# Restoring the previous theme
theme_set(old)