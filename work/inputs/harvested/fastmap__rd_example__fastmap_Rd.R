# r2py crawler metadata
# package: fastmap
# source_type: rd_example
# topic: fastmap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fastmap\help
# lines: 47

suppressPackageStartupMessages(library(fastmap))
# Create the fastmap object
m <- fastmap()

# Set some key-value pairs
m$set("x", 100)
m$set("letters", c("a", "b", "c"))
m$mset(numbers = c(10, 20, 30), nothing = NULL)

# Get values using keys
m$get("x")
m$get("numbers")
m$mget(c("letters", "numbers"))

# Missing keys return NULL by default, but this can be customized
m$get("xyz")

# Check for existence of keys
m$has("x")
m$has("nothing")
m$has("xyz")

# Remove one or more items
m$remove(c("letters", "x"))

# Return number of items
m$size()

# Get all keys
m$keys()

# Return named list that represents all key-value pairs
str(m$as_list())

# Clear the map
m$reset()


# Specify missing value when get() is called
m <- fastmap()
m$get("x", missing = key_missing())
#> <Key Missing>

# Specify the default missing value
m <- fastmap(missing_default = key_missing())
m$get("x")
#> <Key Missing>