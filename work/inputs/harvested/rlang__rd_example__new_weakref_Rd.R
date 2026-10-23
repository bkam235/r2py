# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: new_weakref.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 35

suppressPackageStartupMessages(library(rlang))
e <- env()

# Create a weak reference to e
w <- new_weakref(e, finalizer = function(e) message("finalized"))

# Get the key object from the weak reference
identical(wref_key(w), e)

# When the regular reference (the `e` binding) is removed and a GC occurs,
# the weak reference will not keep the object alive.
rm(e)
gc()
identical(wref_key(w), NULL)


# A weak reference with a key and value. The value contains data about the
# key.
k <- env()
v <- list(1, 2, 3)
w <- new_weakref(k, v)

identical(wref_key(w), k)
identical(wref_value(w), v)

# When v is removed, the weak ref keeps it alive because k is still reachable.
rm(v)
gc()
identical(wref_value(w), list(1, 2, 3))

# When k is removed, the weak ref does not keep k or v alive.
rm(k)
gc()
identical(wref_key(w), NULL)
identical(wref_value(w), NULL)