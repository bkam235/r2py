# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: font_face.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 33

suppressPackageStartupMessages(library(sass))
library(htmltools)

my_font <- list("my-font" = font_google("Pacifico"))
hello <- tags$body(
  "Hello",
  tags$style(
    sass(
      list(
        my_font,
        list("body {font-family: $my-font}")
      )
    )
  )
)

if (interactive()) {
  browsable(hello)
}

# Three different yet equivalent ways of importing a remotely-hosted Google Font
a <- font_google("Crimson Pro", wght = "200..900", local = FALSE)
b <- font_link(
  "Crimson Pro",
  href = "https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@200..900"
)
url <- "https://fonts.gstatic.com/s/crimsonpro/v13/q5uDsoa5M_tv7IihmnkabARboYF6CsKj.woff2"
c <- font_face(
  family = "Crimson Pro",
  style = "normal",
  weight = "200 900",
  src = paste0("url(", url, ") format('woff2')")
)