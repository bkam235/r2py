# r2py crawler metadata
# package: rvest
# source_type: rd_example
# topic: html_element.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\help
# lines: 33

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("
  <h1>This is a heading</h1>
  <p id='first'>This is a paragraph</p>
  <p class='important'>This is an important paragraph</p>
")

html |> html_element("h1")
html |> html_elements("p")
html |> html_elements(".important")
html |> html_elements("#first")

# html_element() vs html_elements() --------------------------------------
html <- minimal_html("
  <ul>
    <li><b>C-3PO</b> is a <i>droid</i> that weighs <span class='weight'>167 kg</span></li>
    <li><b>R2-D2</b> is a <i>droid</i> that weighs <span class='weight'>96 kg</span></li>
    <li><b>Yoda</b> weighs <span class='weight'>66 kg</span></li>
    <li><b>R4-P17</b> is a <i>droid</i></li>
  </ul>
")
li <- html |> html_elements("li")

# When applied to a node set, html_elements() returns all matching elements
# beneath any of the inputs, flattening results into a new node set.
li |> html_elements("i")

# When applied to a node set, html_element() always returns a vector the
# same length as the input, using a "missing" element where needed.
li |> html_element("i")
# and html_text() and html_attr() will return NA
li |> html_element("i") |> html_text2()
li |> html_element("span") |> html_attr("class")