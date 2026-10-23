# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s37
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
guide_key <- function(
  aesthetic, value = aesthetic, label = as.character(aesthetic),
  ...,
  # Standard guide arguments
  theme = NULL, title = waiver(), order = 0, position = waiver()
) {
  
  key <- data.frame(aesthetic, .value = value, .label = label, ...)
  
  new_guide(
    # Arguments passed on to the GuideKey$params field
    key = key, theme = theme, title = title, order = order, position = position,
    # Declare which aesthetics are supported
    available_aes = c("x", "y"),
    # Set the guide class
    super = GuideKey
  )
}