# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: map_depth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 48

suppressPackageStartupMessages(library(purrr))
# map_depth() -------------------------------------------------
# Use `map_depth()` to recursively traverse nested vectors and map
# a function at a certain depth:
x <- list(a = list(foo = 1:2, bar = 3:4), b = list(baz = 5:6))
x |> str()
x |> map_depth(2, \(y) paste(y, collapse = "/")) |> str()

# Equivalent to:
x |> map(\(y) map(y, \(z) paste(z, collapse = "/"))) |> str()

# When ragged is TRUE, `.f()` will also be passed leaves at depth < `.depth`
x <- list(1, list(1, list(1, list(1, 1))))
x |> str()
x |> map_depth(4, \(x) length(unlist(x)), .ragged = TRUE) |> str()
x |> map_depth(3, \(x) length(unlist(x)), .ragged = TRUE) |> str()
x |> map_depth(2, \(x) length(unlist(x)), .ragged = TRUE) |> str()
x |> map_depth(1, \(x) length(unlist(x)), .ragged = TRUE) |> str()
x |> map_depth(0, \(x) length(unlist(x)), .ragged = TRUE) |> str()

# modify_depth() -------------------------------------------------
l1 <- list(
  obj1 = list(
    prop1 = list(param1 = 1:2, param2 = 3:4),
    prop2 = list(param1 = 5:6, param2 = 7:8)
  ),
  obj2 = list(
    prop1 = list(param1 = 9:10, param2 = 11:12),
    prop2 = list(param1 = 12:14, param2 = 15:17)
  )
)

# In the above list, "obj" is level 1, "prop" is level 2 and "param"
# is level 3. To apply sum() on all params, we map it at depth 3:
l1 |> modify_depth(3, sum) |> str()

# modify() lets us pluck the elements prop1/param2 in obj1 and obj2:
l1 |> modify(c("prop1", "param2")) |> str()

# But what if we want to pluck all param2 elements? Then we need to
# act at a lower level:
l1 |> modify_depth(2, "param2") |> str()

# modify_depth() can be with other purrr functions to make them operate at
# a lower level. Here we ask pmap() to map paste() simultaneously over all
# elements of the objects at the second level. paste() is effectively
# mapped at level 3.
l1 |> modify_depth(2, \(x) pmap(x, paste, sep = " / ")) |> str()