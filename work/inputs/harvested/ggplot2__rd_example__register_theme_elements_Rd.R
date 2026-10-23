# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: register_theme_elements.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 29

suppressPackageStartupMessages(library(ggplot2))
# Let's assume a package `ggxyz` wants to provide an easy way to add annotations to
# plot panels. To do so, it registers a new theme element `ggxyz.panel.annotation`
register_theme_elements(
  ggxyz.panel.annotation = element_text(color = "blue", hjust = 0.95, vjust = 0.05),
  element_tree = list(ggxyz.panel.annotation = el_def(element_text, "text"))
)

# Now the package can define a new coord that includes a panel annotation
coord_annotate <- function(label = "panel annotation") {
  ggproto(NULL, CoordCartesian,
    limits = list(x = NULL, y = NULL),
    expand = TRUE,
    default = FALSE,
    clip = "on",
    render_fg = function(panel_params, theme) {
      element_render(theme, "ggxyz.panel.annotation", label = label)
    }
  )
}

# Example plot with this new coord
df <- data.frame(x = 1:3, y = 1:3)
ggplot(df, aes(x, y)) +
  geom_point() +
  coord_annotate("annotation in blue")

# Revert to the original ggplot2 settings
reset_theme_settings()