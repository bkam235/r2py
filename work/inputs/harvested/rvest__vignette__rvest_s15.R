# r2py crawler metadata
# package: rvest
# source_type: vignette
# topic: rvest_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rvest\doc\rvest.R
# lines: 21

suppressPackageStartupMessages(library(rvest))
html <- minimal_html("
  <table>
    <tr>
      <th>x</th>
      <th>y</th>
    </tr>
    <tr>
      <td>1.5</td>
      <td>2.7</td>
    </tr>
    <tr>
      <td>4.9</td>
      <td>1.3</td>
    </tr>
    <tr>
      <td>7.2</td>
      <td>8.1</td>
    </tr>
  </table>
  ")