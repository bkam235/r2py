# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: builder.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 29

suppressPackageStartupMessages(library(htmltools))
tags$html(
  tags$head(
    tags$title('My first page')
  ),
  tags$body(
    h1('My first heading'),
    p('My first paragraph, with some ', strong('bold'), ' text.'),
    div(
      id = 'myDiv', class = 'simpleDiv',
      'Here is a div with some attributes.'
     )
  )
)

# html5 <audio> with boolean control attribute
# https://www.w3.org/TR/html5/infrastructure.html#sec-boolean-attributes
tags$audio(
  controls = NA,
  tags$source(
    src = "myfile.wav",
    type = "audio/wav"
  )
)

# suppress the whitespace between tags
tags$span(
  tags$strong("I'm strong", .noWS="outside")
)