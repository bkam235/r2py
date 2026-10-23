# r2py crawler metadata
# package: sys
# source_type: rd_example
# topic: exec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sys\help
# lines: 22

suppressPackageStartupMessages(library(sys))
# Run a command (interrupt with CTRL+C)
status <- exec_wait("date")

# Capture std/out
out <- exec_internal("date")
print(out$status)
cat(as_text(out$stdout))

if(nchar(Sys.which("ping"))){

# Run a background process (daemon)
pid <- exec_background("ping", "localhost")

# Kill it after a while
Sys.sleep(2)
tools::pskill(pid)

# Cleans up the zombie proc
exec_status(pid)
rm(pid)
}