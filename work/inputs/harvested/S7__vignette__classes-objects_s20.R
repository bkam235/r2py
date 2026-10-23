# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 16

suppressPackageStartupMessages(library(S7))
Person <- new_class("Person", properties = list(
 birth_date = new_property(
   class_Date,
   setter = function(self, value) {
     if(!is.null(self@birth_date)) {
       stop("@birth_date is read-only", call. = FALSE)
     }
     self@birth_date <- as.Date(value)
     self
   }
)))

person <- Person("1999-12-31")

try(person@birth_date <- "2000-01-01")