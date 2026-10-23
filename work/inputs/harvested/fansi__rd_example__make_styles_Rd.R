# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: make_styles.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 35

suppressPackageStartupMessages(library(fansi))
## Generate some class strings; order matters
classes <- do.call(paste, c(expand.grid(c("fg", "bg"), 0:7), sep="-"))
writeLines(classes[1:4])

## Some Default CSS
css0 <- "span {font-size: 60pt; padding: 10px; display: inline-block}"

## Associated class strings to styles
css1 <- make_styles(classes)
writeLines(css1[1:4])

## Generate SGR-derived HTML, mapping to classes
string <- "\033[43mYellow\033[m\n\033[45mMagenta\033[m\n\033[46mCyan\033[m"
html <- to_html(string, classes=classes)
writeLines(html)

## Combine in a page with styles and display in browser

in_html(html, css=c(css0, css1))


## Change CSS by remixing colors, and apply to exact same HTML
mix <- matrix(
  c(
    0, 1, 0,  # red output is green input
    0, 0, 1,  # green output is blue input
    1, 0, 0   # blue output is red input
  ),
  nrow=3, byrow=TRUE
)
css2 <- make_styles(classes, rgb.mix=mix)
## Display in browser: same HTML but colors changed by CSS

in_html(html, css=c(css0, css2))