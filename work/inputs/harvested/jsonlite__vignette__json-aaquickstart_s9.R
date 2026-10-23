# r2py crawler metadata
# package: jsonlite
# source_type: vignette
# topic: json-aaquickstart_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\jsonlite\doc\json-aaquickstart.R
# lines: 12

suppressPackageStartupMessages(library(jsonlite))
json <- '[
   [[1, 2], 
    [3, 4]],
   [[5, 6], 
    [7, 8]],
   [[9, 10],
    [11, 12]]
]'
myarray <- fromJSON(json)
myarray[1, , ]
myarray[ , ,1]