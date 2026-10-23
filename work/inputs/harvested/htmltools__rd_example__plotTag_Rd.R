# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: plotTag.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 16

suppressPackageStartupMessages(library(htmltools))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
img <- plotTag({
  plot(cars)
}, "A plot of the 'cars' dataset", width = 375, height = 275)

img

if (capabilities("cairo")) {
  plotTag(
    plot(pressure), "A plot of the 'pressure' dataset",
    device = grDevices::svg, width = 375, height = 275, pixelratio = 1/72,
    mimeType = "image/svg+xml"
  )
}
}) # examplesIf