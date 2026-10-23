# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: file_temp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 19

suppressPackageStartupMessages(library(fs))
file_temp_push("/tmp/filedd461c46df20")

path_temp()
path_temp("does-not-exist")

file_temp()
file_temp(ext = "png")
file_temp("image", ext = "png")


# You can make the temp file paths deterministic
file_temp_push(letters)
file_temp()
file_temp()

# Or explicitly remove values
while (!is.null(file_temp_pop())) next
file_temp_pop()