# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 25

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "Scatterplot of engine displacement versus highway miles per
#|  gallon, for 234 cars. A wobbly line follows the point cloud over the 
#|  horizontal direction. 20 points are placed on top of the line with constant
#|  horizontal intervals."
StatLm <- ggproto("StatLm", Stat, 
  required_aes = c("x", "y"),
  
  compute_group = function(data, scales, params = list(), n = 100, formula = y ~ x) {
    rng <- range(data$x, na.rm = TRUE)
    grid <- data.frame(x = seq(rng[1], rng[2], length = n))
    
    mod <- lm(formula, data = data)
    grid$y <- predict(mod, newdata = grid)
    
    grid
  }
)

stat_lm <- make_constructor(StatLm, geom = "line")

ggplot(mpg, aes(displ, hwy)) + 
  geom_point() + 
  stat_lm(formula = y ~ poly(x, 10)) + 
  stat_lm(formula = y ~ poly(x, 10), geom = "point", colour = "red", n = 20)