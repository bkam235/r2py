# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: tojson.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 13

library(xfun)
tojson(NULL)
tojson(1:10)
tojson(TRUE)
tojson(FALSE)
tojson(list(a = 1, b = list(c = 1:3, d = "abc")))
tojson(list(c("a", "b"), 1:5, TRUE, Sys.Date() + 1:3))
tojson(head(iris))  # each column is in an element
tojson(unname(head(iris)))  # each row is in an element
tojson(matrix(1:12, 3))

# literal JS code
tojson(list(a = 1:5, b = js("function() {return true;}")))