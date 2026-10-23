# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 10

suppressPackageStartupMessages(library(S7))
Person <- new_class("Person", properties = list(
 name = new_property(
   class_character,
   default = quote(stop("@name is required")))
))

try(Person())

Person("Alice")