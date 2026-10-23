# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 16

suppressPackageStartupMessages(library(S7))
Person <- new_class("Person", properties = list(
 name = new_property(
   class_character,
   validator = function(value) {
     if (length(value) != 1 || is.na(value) || value == "")
       "must be a non-empty string"
   }
 )
))

try(Person())

try(Person(1)) # class_character$validator() is also checked.

Person("Alice")