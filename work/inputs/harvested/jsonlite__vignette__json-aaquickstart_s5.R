# r2py crawler metadata
# package: jsonlite
# source_type: vignette
# topic: json-aaquickstart_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\doc\json-aaquickstart.R
# lines: 10

suppressPackageStartupMessages(library(jsonlite))
json <-
'[
  {"Name" : "Mario", "Age" : 32, "Occupation" : "Plumber"}, 
  {"Name" : "Peach", "Age" : 21, "Occupation" : "Princess"},
  {},
  {"Name" : "Bowser", "Occupation" : "Koopa"}
]'
mydf <- fromJSON(json)
mydf