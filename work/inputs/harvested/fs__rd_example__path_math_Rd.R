# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path_math.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 32

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
dir_create("a")
file_create("a/b")
link_create(path_abs("a"), "c")

# Realize the path
path_real("c/b")

# Split a path
parts <- path_split("a/b")
parts

# Join it together
path_join(parts)

# Find the absolute path
path_abs("..")

# Normalize a path
path_norm("a/../b\\c/.")

# Compute a relative path
path_rel("/foo/abc", "/foo/bar/baz")

# Find the common path between multiple paths
path_common(c("/foo/bar/baz", "/foo/bar/abc", "/foo/xyz/123"))

# Cleanup
dir_delete("a")
link_delete("c")
setwd(.old_wd)