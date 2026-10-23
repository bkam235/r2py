# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: get_theme.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 39

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mtcars, aes(mpg, wt)) +
  geom_point()
p

# Use set_theme() to completely override the current theme.
# update_theme() and replace_theme() are similar except they
# apply directly to the current/active theme.
# update_theme() modifies a particular element of the current theme.
# Here we have the old theme so we can later restore it.
# Note that the theme is applied when the plot is drawn, not
# when it is created.
old <- set_theme(theme_bw())
p

set_theme(old)
update_theme(panel.grid.minor = element_line(colour = "red"))
p

set_theme(old)
replace_theme(panel.grid.minor = element_line(colour = "red"))
p

set_theme(old)
p


# Modifying theme objects -----------------------------------------
# You can use + and %+replace% to modify a theme object.
# They differ in how they deal with missing arguments in
# the theme elements.

add_el <- theme_grey() +
  theme(text = element_text(family = "Times"))
add_el$text

rep_el <- theme_grey() %+replace%
  theme(text = element_text(family = "Times"))
rep_el$text