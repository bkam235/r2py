# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: stamp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 13

suppressPackageStartupMessages(library(lubridate))
D <- ymd("2010-04-05") - days(1:5)
stamp("March 1, 1999")(D)
sf <- stamp("Created on Sunday, Jan 1, 1999 3:34 pm")
sf(D)
stamp("Jan 01")(D)
stamp("Sunday, May 1, 2000", locale = "C")(D)
stamp("Sun Aug 5")(D) #=> "Sun Aug 04" "Sat Aug 04" "Fri Aug 04" "Thu Aug 04" "Wed Aug 03"
stamp("12/31/99")(D)              #=> "06/09/11"
stamp("Sunday, May 1, 2000 22:10", locale = "C")(D)
stamp("2013-01-01T06:00:00Z")(D)
stamp("2013-01-01T00:00:00-06")(D)
stamp("2013-01-01T00:00:00-08:00")(force_tz(D, "America/Chicago"))