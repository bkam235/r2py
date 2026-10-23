# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s34
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 52

suppressPackageStartupMessages(library(ggplot2))
#| fig.alt: "Scatterplot with three-by-three panels showing the weight versus
#|  the price of about 10.000 diamonds in every panel. The panels are titled 1
#|  to 9 and show different points, but are visually similar."

facet_bootstrap <- function(n = 9, prop = 0.2, nrow = NULL, ncol = NULL, 
  scales = "fixed", shrink = TRUE, strip.position = "top") {
  
  facet <- facet_wrap(~.bootstrap, nrow = nrow, ncol = ncol, scales = scales, 
    shrink = shrink, strip.position = strip.position)
  facet$params$n <- n
  facet$params$prop <- prop
  ggproto(NULL, FacetBootstrap,
    shrink = shrink,
    params = facet$params
  )
}

FacetBootstrap <- ggproto("FacetBootstrap", FacetWrap,
  compute_layout = function(data, params) {
    id <- seq_len(params$n)

    dims <- wrap_dims(params$n, params$nrow, params$ncol)
    layout <- data.frame(PANEL = factor(id))

    layout$ROW <- as.integer((id - 1L) %/% dims[2] + 1L)
    layout$COL <- as.integer((id - 1L) %% dims[2] + 1L)

    layout <- layout[order(layout$PANEL), , drop = FALSE]
    rownames(layout) <- NULL

    # Add scale identification
    layout$SCALE_X <- if (params$free$x) id else 1L
    layout$SCALE_Y <- if (params$free$y) id else 1L

    cbind(layout, .bootstrap = id)
  },
  map_data = function(data, layout, params) {
    if (is.null(data) || nrow(data) == 0) {
      return(cbind(data, PANEL = integer(0)))
    }
    n_samples <- round(nrow(data) * params$prop)
    new_data <- lapply(seq_len(params$n), function(i) {
      cbind(data[sample(nrow(data), n_samples), , drop = FALSE], PANEL = i)
    })
    do.call(rbind, new_data)
  }
)

ggplot(diamonds, aes(carat, price)) + 
  geom_point(alpha = 0.1) + 
  facet_bootstrap(n = 9, prop = 0.05)