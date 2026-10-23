# r2py crawler metadata
# package: rvest
# source_type: rd_example
# topic: html_attr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\help
# lines: 12

suppressPackageStartupMessages(library(rvest))
html <- minimal_html('<ul>
  <li><a href="https://a.com" class="important">a</a></li>
  <li class="active"><a href="https://c.com">b</a></li>
  <li><a href="https://c.com">b</a></li>
  </ul>')

html |> html_elements("a") |> html_attrs()

html |> html_elements("a") |> html_attr("href")
html |> html_elements("li") |> html_attr("class")
html |> html_elements("li") |> html_attr("class", default = "inactive")