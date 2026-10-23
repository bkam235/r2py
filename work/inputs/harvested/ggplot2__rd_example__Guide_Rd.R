# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: Guide.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 42

suppressPackageStartupMessages(library(ggplot2))
# Extending the class
GuideDescribe <- ggproto(
  "GuideDescribe", Guide,
  # Fields
  elements  = list(text = "legend.text", margin = "legend.margin"),
  hashables = rlang::exprs(key$.label),

  # Methods
  build_title = function(...) zeroGrob(), # Turn off title

  build_labels = function(key, elements, params) {
    labels <- key$.label
    n <- length(labels)
    labels <- paste0(paste0(labels[-n], collapse = ", "), ", and ", labels[n])
    labels <- paste0("A guide showing ", labels, " categories")
    element_grob(elements$text, label = labels, margin_x = TRUE, margin_y = TRUE)
  },

  measure_grobs = function(grobs, params, elements) {
    # Measuring in centimetres is the convention
    width  <- grid::convertWidth(grid::grobWidth(grobs$labels), "cm", valueOnly = TRUE)
    height <- grid::convertHeight(grid::grobHeight(grobs$labels), "cm", valueOnly = TRUE)
    list(width = unit(width, "cm"), height = unit(height, "cm"))
  },

  assemble_drawing = function(self, grobs, layout, sizes, params, elements) {
    gt <- gtable::as.gtable(grobs$labels, width = sizes$width, height = sizes$height)
    gt <- gtable::gtable_add_padding(gt, elements$margin)
    gt
  }
)

# Building a constructor
guide_describe <- function(position = NULL) {
  new_guide(position = position, super = GuideDescribe)
}

# Use new guide plot
ggplot(mpg, aes(displ, hwy, colour = class)) +
  geom_point() +
  guides(colour = guide_describe("bottom"))