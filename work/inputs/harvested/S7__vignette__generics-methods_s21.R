# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 20

suppressPackageStartupMessages(library(S7))
Pet <- new_class("Pet")
Dog <- new_class("Dog", Pet)
Cat <- new_class("Cat", Pet)

Language <- new_class("Language")
English <- new_class("English", Language)
French <- new_class("French", Language)

speak <- new_generic("speak", c("x", "y"))
method(speak, list(Dog, English)) <- function(x, y) "Woof"
method(speak, list(Cat, English)) <- function(x, y) "Meow"
method(speak, list(Dog, French)) <- function(x, y) "Ouaf Ouaf"
method(speak, list(Cat, French)) <- function(x, y) "Miaou"

speak(Cat(), English())
speak(Dog(), French())

# This example was originally inspired by blog.klipse.tech/javascript/2021/10/03/multimethod.html
# which has unfortunately since disappeared.