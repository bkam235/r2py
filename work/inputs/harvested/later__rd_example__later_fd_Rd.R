# r2py crawler metadata
# package: later
# source_type: rd_example
# topic: later_fd.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\later\help
# lines: 38

suppressPackageStartupMessages(library(later))
if (requireNamespace("nanonext", quietly = TRUE)) withAutoprint({ # examplesIf
# create nanonext sockets
s1 <- nanonext::socket(listen = "inproc://nano")
s2 <- nanonext::socket(dial = "inproc://nano")
fd1 <- nanonext::opt(s1, "recv-fd")
fd2 <- nanonext::opt(s2, "recv-fd")

# 1. timeout: prints FALSE, FALSE
later_fd(print, c(fd1, fd2), timeout = 0.1)
Sys.sleep(0.2)
run_now()

# 2. fd1 ready: prints TRUE, FALSE
later_fd(print, c(fd1, fd2), timeout = 1)
res <- nanonext::send(s2, "msg")
Sys.sleep(0.1)
run_now()

# 3. both ready: prints TRUE, TRUE
res <- nanonext::send(s1, "msg")
later_fd(print, c(fd1, fd2), timeout = 1)
Sys.sleep(0.1)
run_now()

# 4. fd2 ready: prints FALSE, TRUE
res <- nanonext::recv(s1)
later_fd(print, c(fd1, fd2), timeout = 1)
Sys.sleep(0.1)
run_now()

# 5. fds invalid: prints NA, NA
close(s2)
close(s1)
later_fd(print, c(fd1, fd2), timeout = 0)
Sys.sleep(0.1)
run_now()
}) # examplesIf