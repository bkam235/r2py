# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 36

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt:
#| - "A line plot showing three kernel density estimates of engine displacement,
#|  coloured for three types of drive trains. The lines are a little bit 
#|  wobbly."
#| - "A line plot showing three kernel density estimates of engine displacement,
#|  coloured for three types of drive trains. The lines are fairly smooth."
StatDensityCommon <- ggproto("StatDensityCommon", Stat, 
  required_aes = "x",
  
  setup_params = function(data, params) {
    if (!is.null(params$bandwidth))
      return(params)
    
    xs <- split(data$x, data$group)
    bws <- vapply(xs, bw.nrd0, numeric(1))
    bw <- mean(bws)
    message("Picking bandwidth of ", signif(bw, 3))
    
    params$bandwidth <- bw
    params
  },
  
  compute_group = function(data, scales, bandwidth = 1) {
    d <- density(data$x, bw = bandwidth)
    data.frame(x = d$x, y = d$y)
  }  
)

stat_density_common <- make_constructor(StatDensityCommon, geom = "line")

ggplot(mpg, aes(displ, colour = drv)) + 
  stat_density_common()

ggplot(mpg, aes(displ, colour = drv)) + 
  stat_density_common(bandwidth = 0.5)