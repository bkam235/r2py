# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s39
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 27

suppressPackageStartupMessages(library(ggplot2))
#| label: key_ggproto_edit
# Same as before
GuideKey <- ggproto(
  "Guide", GuideAxis,
  params = c(GuideAxis$params, list(key = NULL)),
  extract_key = function(scale, aesthetic, key, ...) {
    key$aesthetic <- scale$map(key$aesthetic)
    names(key)[names(key) == "aesthetic"] <- aesthetic
    key
  },
  
  # New method to draw labels
  build_labels = function(key, elements, params) {
    position <- params$position
    # Downstream code expects a list of labels
    list(element_grob(
      elements$text,
      label = key$.label,
      x = switch(position, left = 1, right = 0, key$x),
      y = switch(position, top = 0, bottom = 1, key$y),
      margin_x = position %in% c("left", "right"),
      margin_y = position %in% c("top", "bottom"),
      colour = key$colour
    ))
  }
)