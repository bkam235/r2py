# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: bindFillRole.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 24

suppressPackageStartupMessages(library(htmltools))
tagz <- div(
  id = "outer",
  style = css(
    height = "600px",
    border = "3px red solid"
  ),
  div(
    id = "inner",
    style = css(
      height = "400px",
      border = "3px blue solid"
    )
  )
)

# Inner doesn't fill outer
if (interactive()) browsable(tagz)

tagz <- bindFillRole(tagz, container = TRUE)
tagz <- bindFillRole(tagz, item = TRUE, .cssSelector = "#inner")

# Inner does fill outer
if (interactive()) browsable(tagz)