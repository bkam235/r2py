# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: aes_colour_fill_alpha.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 54

suppressPackageStartupMessages(library(ggplot2))
# Bar chart example
p <- ggplot(mtcars, aes(factor(cyl)))
# Default plotting
p + geom_bar()
# To change the interior colouring use fill aesthetic
p + geom_bar(fill = "red")
# Compare with the colour aesthetic which changes just the bar outline
p + geom_bar(colour = "red")
# Combining both, you can see the changes more clearly
p + geom_bar(fill = "white", colour = "red")
# Both colour and fill can take an rgb specification.
p + geom_bar(fill = "#00abff")
# Use NA for a completely transparent colour.
p + geom_bar(fill = NA, colour = "#00abff")

# Colouring scales differ depending on whether a discrete or
# continuous variable is being mapped. For example, when mapping
# fill to a factor variable, a discrete colour scale is used.
ggplot(mtcars, aes(factor(cyl), fill = factor(vs))) + geom_bar()

# When mapping fill to continuous variable a continuous colour
# scale is used.
ggplot(faithfuld, aes(waiting, eruptions)) +
  geom_raster(aes(fill = density))

# Some geoms only use the colour aesthetic but not the fill
# aesthetic (e.g. geom_point() or geom_line()).
p <- ggplot(economics, aes(x = date, y = unemploy))
p + geom_line()
p + geom_line(colour = "green")
p + geom_point()
p + geom_point(colour = "red")

# For large datasets with overplotting the alpha
# aesthetic will make the points more transparent.
set.seed(1)
df <- data.frame(x = rnorm(5000), y = rnorm(5000))
p  <- ggplot(df, aes(x,y))
p + geom_point()
p + geom_point(alpha = 0.5)
p + geom_point(alpha = 1/10)

# Alpha can also be used to add shading.
p <- ggplot(economics, aes(x = date, y = unemploy)) + geom_line()
p
yrng <- range(economics$unemploy)
p <- p +
  geom_rect(
    aes(NULL, NULL, xmin = start, xmax = end, fill = party),
    ymin = yrng[1], ymax = yrng[2], data = presidential
  )
p
p + scale_fill_manual(values = alpha(c("blue", "red"), .3))