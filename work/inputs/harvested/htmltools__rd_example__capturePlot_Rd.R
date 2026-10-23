# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: capturePlot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 29

suppressPackageStartupMessages(library(htmltools))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
# Default settings
res <- capturePlot(plot(cars))

# View result
browseURL(res)

# Clean up
unlink(res)

# Custom width/height
pngpath <- tempfile(fileext = ".png")
capturePlot(plot(pressure), pngpath, width = 800, height = 375)
browseURL(pngpath)
unlink(pngpath)

# Use a custom graphics device (e.g., SVG)
if (capabilities("cairo")) {
  svgpath <- capturePlot(
    plot(pressure),
    tempfile(fileext = ".svg"),
    grDevices::svg,
    width = 8, height = 3.75
  )
  browseURL(svgpath)
  unlink(svgpath)
}
}) # examplesIf