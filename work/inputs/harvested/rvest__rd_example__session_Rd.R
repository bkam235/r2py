# r2py crawler metadata
# package: rvest
# source_type: rd_example
# topic: session.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\help
# lines: 16

suppressPackageStartupMessages(library(rvest))
s <- session("http://hadley.nz")
s |>
  session_jump_to("hadley.jpg") |>
  session_jump_to("/") |>
  session_history()

s |>
  session_jump_to("hadley.jpg") |>
  session_back() |>
  session_history()


s |>
  session_follow_link(css = "p a") |>
  html_elements("p")