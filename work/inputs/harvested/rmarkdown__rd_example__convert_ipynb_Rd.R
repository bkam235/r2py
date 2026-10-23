# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: convert_ipynb.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 18

suppressPackageStartupMessages(library(rmarkdown))
# this is not a real ipynb file, but illustrates what convert_ipynb() does
nb_data <- list(
  cells = list(
    list(cell_type = 'markdown', source = 'Hi **Markdown**!'),
    list(cell_type = 'code', source = 'print("Hi R Markdown!")')
  ),
  metadata = list(
    kernelspec = list(language = 'python')
  )
)
nb_file = tempfile(fileext = '.ipynb')
jsonlite::write_json(nb_data, nb_file, auto_unbox = TRUE, pretty = TRUE)
xfun::file_string(nb_file)  # show file content

# convert to R Markdown
nb_rmd = rmarkdown:::convert_ipynb(nb_file)
xfun::file_string(nb_rmd)