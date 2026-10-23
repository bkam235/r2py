# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: sass_layer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 45

suppressPackageStartupMessages(library(sass))
blue <- list(color = "blue !default")
red <- list(color = "red !default")
green <- list(color = "green !default")

# a sass_layer() by itself is not very useful, it just defines some
# SASS to place before (defaults) and after (rules)
core <- sass_layer(defaults = blue, rules = "body { color: $color; }")
core
sass(core)

# However, by stacking sass_layer()s, we have ability to place
# SASS both before and after some other sass (e.g., core)
# Here we place a red default _before_ the blue default and export the
# color SASS variable as a CSS variable _after_ the core
red_layer <- sass_layer(red, rules = ":root{ --color: #{$color}; }")
sass(sass_bundle(core, red_layer))
sass(sass_bundle(core, red_layer, sass_layer(green)))

# Example of merging layers and removing a layer
# Remember to name the layers that are removable
core_layers <- sass_bundle(core, red = red_layer, green = sass_layer(green))
core_layers # pretty printed for console
core_slim <- sass_bundle_remove(core_layers, "red")
sass(core_slim)


# File attachment example: Create a checkboard pattern .png, then
# use it from a sass layer

tmp_png <- tempfile(fileext = ".png")
grDevices::png(filename = tmp_png, width = 20, height = 20,
  bg = "transparent", antialias = "none")
par(mar = rep_len(0,4), xaxs = "i", yaxs = "i")
plot.new()
rect(c(0,0.5), c(0,0.5), c(0.5,1), c(0.5,1), col = "#00000044", border=NA)
dev.off()

layer <- sass_layer(
  rules = ".bg-check { background-image: url(images/demo_checkboard_bg.png) }",
  file_attachments = c("images/demo_checkboard_bg.png" = tmp_png)
)

output_path <- tempfile(fileext = ".css")
sass(layer, output = output_path, write_attachments = TRUE)