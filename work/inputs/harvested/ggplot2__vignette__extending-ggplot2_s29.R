# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 67

suppressPackageStartupMessages(library(ggplot2))
render <- function(panels, layout, x_scales, y_scales, ranges, coord, data,
                   theme, params) {
  # Place panels according to settings
  if (params$horizontal) {
    # Put panels in matrix and convert to a gtable
    panels <- matrix(panels, ncol = 2)
    panel_table <- gtable::gtable_matrix("layout", panels, 
      widths = unit(c(1, 1), "null"), heights = unit(1, "null"), clip = "on")
    # Add spacing according to theme
    panel_spacing <- calc_element("panel.spacing.x", theme)
    panel_table <- gtable::gtable_add_col_space(panel_table, panel_spacing)
  } else {
    panels <- matrix(panels, ncol = 1)
    panel_table <- gtable::gtable_matrix("layout", panels, 
      widths = unit(1, "null"), heights = unit(c(1, 1), "null"), clip = "on")
    panel_spacing <- if (is.null(theme$panel.spacing.y)) {
      theme$panel.spacing
    } else {
      theme$panel.spacing.y
    }
    panel_table <- gtable::gtable_add_row_space(panel_table, panel_spacing)
  }
  # Name panel grobs so they can be found later
  panel_table$layout$name <- paste0("panel-", c(1, 2))
  
  # Construct the axes
  axes <- render_axes(ranges[1], ranges[1], coord, theme, 
    transpose = TRUE)

  # Add axes around each panel
  panel_pos_h <- panel_cols(panel_table)$l
  panel_pos_v <- panel_rows(panel_table)$t
  axis_width_l <- unit(grid::convertWidth(
    grid::grobWidth(axes$y$left[[1]]), "cm", TRUE), "cm")
  axis_width_r <- unit(grid::convertWidth(
    grid::grobWidth(axes$y$right[[1]]), "cm", TRUE), "cm")
  ## We do it reverse so we don't change the position of panels when we add axes
  for (i in rev(panel_pos_h)) {
    panel_table <- gtable::gtable_add_cols(panel_table, axis_width_r, i)
    panel_table <- gtable::gtable_add_grob(panel_table, 
      rep(axes$y$right, length(panel_pos_v)), t = panel_pos_v, l = i + 1, 
      clip = "off")
    panel_table <- gtable::gtable_add_cols(panel_table, axis_width_l, i - 1)
    panel_table <- gtable::gtable_add_grob(panel_table, 
      rep(axes$y$left, length(panel_pos_v)), t = panel_pos_v, l = i, 
      clip = "off")
  }
  ## Recalculate as gtable has changed
  panel_pos_h <- panel_cols(panel_table)$l
  panel_pos_v <- panel_rows(panel_table)$t
  axis_height_t <- unit(grid::convertHeight(
    grid::grobHeight(axes$x$top[[1]]), "cm", TRUE), "cm")
  axis_height_b <- unit(grid::convertHeight(
    grid::grobHeight(axes$x$bottom[[1]]), "cm", TRUE), "cm")
  for (i in rev(panel_pos_v)) {
    panel_table <- gtable::gtable_add_rows(panel_table, axis_height_b, i)
    panel_table <- gtable::gtable_add_grob(panel_table, 
      rep(axes$x$bottom, length(panel_pos_h)), t = i + 1, l = panel_pos_h, 
      clip = "off")
    panel_table <- gtable::gtable_add_rows(panel_table, axis_height_t, i - 1)
    panel_table <- gtable::gtable_add_grob(panel_table, 
      rep(axes$x$top, length(panel_pos_h)), t = i, l = panel_pos_h, 
      clip = "off")
  }
  panel_table
}