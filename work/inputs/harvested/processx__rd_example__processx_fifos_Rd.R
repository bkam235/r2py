# r2py crawler metadata
# package: processx
# source_type: rd_example
# topic: processx_fifos.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\processx\help
# lines: 27

suppressPackageStartupMessages(library(processx))
# Example for a non-blocking FIFO

# Need to open the reading end first, otherwise Unix fails
reader <- conn_create_fifo()

# Always use poll() before you read, with a timeout if you like.
# If you read before the other end of the FIFO is connected, then
# the OS (or processx?) assumes that the FIFO is done, and you cannot
# read anything.
# Now poll() tells us that there is no data yet.
poll(list(reader), 0)

writer <- conn_connect_fifo(conn_file_name(reader), write = TRUE)
conn_write(writer, "hello\nthere!\n")

poll(list(reader), 1000)
conn_read_lines(reader, 1)
conn_read_chars(reader)

conn_is_incomplete(reader)

close(writer)
conn_read_chars(reader)
conn_is_incomplete(reader)

close(reader)