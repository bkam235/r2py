# r2py crawler metadata
# package: uuid
# source_type: rd_example
# topic: UUID.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\uuid\help
# lines: 12

suppressPackageStartupMessages(library(uuid))
(u <- as.UUID("837bc850-07d9-42f9-9afb-716409bf87b7"))
(uv <- c(u, NA, UUIDgenerate(n=3, output="uuid")))
as.character(u)
uv == u
is.na(uv)
identical(as.UUID(as.character(uv)), uv)
as.raw(u)

## all forms are can be coerced losslessly
identical(as.UUID(as.raw(uv)), uv)
identical(as.UUID(as.character(as.UUID(as.raw(uv)))), uv)