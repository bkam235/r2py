# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s36
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 16

suppressPackageStartupMessages(library(ggplot2))
GuideKey <- ggproto(
  "Guide", GuideAxis,
  
  # Some parameters are required, so it is easiest to copy the base Guide's
  # parameters into our new parameters.
  # We add a new 'key' parameter for our own guide.
  params = c(GuideAxis$params, list(key = NULL)),
  
  # It is important for guides to have a mapped aesthetic with the correct name
  extract_key = function(scale, aesthetic, key, ...) {
    key$aesthetic <- scale$map(key$aesthetic)
    names(key)[names(key) == "aesthetic"] <- aesthetic
    key
  }
)