# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: freePort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 26

suppressPackageStartupMessages(library(parallelly))
# Make sure to undo any changes at the end
oenv <- Sys.getenv("R_PARALLELLY_RANDOM_PORTS")

# Get a random, free TCP port in 1024:65535
port <- freePort()
message("A free TCP port: ", port)

# Get a random, free TCP port in 11000:11999, which is what
# parallelly::makeClusterPSOCK() and parallel::makePSOCKcluster()
# default to (but the latter does not make sure it is available)
Sys.unsetenv("R_PARALLELLY_RANDOM_PORTS")
port <- freePort("random")
message("A free TCP port: ", port)

# Customize the range of ports to sample from to 30000:50000
Sys.setenv(R_PARALLELLY_RANDOM_PORTS = "30000:50000")
port <- freePort("random")
message("A free TCP port: ", port)

# Test if a specific port is free
isPortFree <- function(port) !is.na(freePort(port, default = NA_integer_))
message("TCP port 1024 is free: ", isPortFree(1024))

# Undo changes
Sys.setenv(R_PARALLELLY_RANDOM_PORTS = oenv)