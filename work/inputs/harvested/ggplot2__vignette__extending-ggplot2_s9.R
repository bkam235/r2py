# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 23

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "Scatterplot of engine displacement versus highway miles per
#|  gallon, for 234 cars. A straight line with a negative slope passes through
#|  the cloud of points."
StatLm <- ggproto("StatLm", Stat, 
  required_aes = c("x", "y"),
  
  compute_group = function(data, scales) {
    rng <- range(data$x, na.rm = TRUE)
    grid <- data.frame(x = rng)
    
    mod <- lm(y ~ x, data = data)
    grid$y <- predict(mod, newdata = grid)
    
    grid
  }
)

stat_lm <- make_constructor(StatLm, geom = "line")

ggplot(mpg, aes(displ, hwy)) + 
  geom_point() + 
  stat_lm()