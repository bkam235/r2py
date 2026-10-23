# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 32

suppressPackageStartupMessages(library(S7))
Person <- new_class("Person", properties = list(
 first_name = class_character,
 firstName = new_property(
    class_character,
    default = quote(first_name),
    getter = function(self) {
      warning("@firstName is deprecated; please use @first_name instead", call. = FALSE)
      self@first_name
    },
    setter = function(self, value) {
      if (identical(value, self@first_name)) {
        return(self)
      }
      warning("@firstName is deprecated; please use @first_name instead", call. = FALSE)
      self@first_name <- value
      self
    }
  )
))

args(Person)

hadley <- Person(firstName = "Hadley")

hadley <- Person(first_name = "Hadley") # no warning

hadley@firstName

hadley@firstName <- "John"

hadley@first_name  # no warning