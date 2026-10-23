# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: new_property.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 27

suppressPackageStartupMessages(library(S7))
# Simple properties store data inside an object
Pizza <- new_class("Pizza", properties = list(
  slices = new_property(class_numeric, default = 10)
))
my_pizza <- Pizza(slices = 6)
my_pizza@slices
my_pizza@slices <- 5
my_pizza@slices

your_pizza <- Pizza()
your_pizza@slices

# Dynamic properties can compute on demand
Clock <- new_class("Clock", properties = list(
  now = new_property(getter = function(self) Sys.time())
))
my_clock <- Clock()
my_clock@now; Sys.sleep(1)
my_clock@now
# This property is read only, because there is a 'getter' but not a 'setter'
try(my_clock@now <- 10)

# Because the property is dynamic, it is not included as an
# argument to the default constructor
try(Clock(now = 10))
args(Clock)