# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_rug.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 34

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mtcars, aes(wt, mpg)) +
  geom_point()
p
p + geom_rug()
p + geom_rug(sides="b")    # Rug on bottom only
p + geom_rug(sides="trbl") # All four sides

# Use jittering to avoid overplotting for smaller datasets
ggplot(mpg, aes(displ, cty)) +
  geom_point() +
  geom_rug()

ggplot(mpg, aes(displ, cty)) +
  geom_jitter() +
  geom_rug(alpha = 1/2, position = "jitter")

# move the rug tassels to outside the plot
# remember to set clip = "off".
p +
  geom_rug(outside = TRUE) +
  coord_cartesian(clip = "off")

# set sides to top right, and then move the margins
p +
  geom_rug(outside = TRUE, sides = "tr") +
  coord_cartesian(clip = "off") +
  theme(plot.margin = margin_auto(1, unit = "cm"))

# increase the line length and
# expand axis to avoid overplotting
p +
  geom_rug(length = unit(0.05, "npc")) +
  scale_y_continuous(expand = c(0.1, 0.1))