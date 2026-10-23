# r2py crawler metadata
# package: farver
# source_type: rd_example
# topic: manip_channel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\farver\help
# lines: 23

suppressPackageStartupMessages(library(farver))
spectrum <- rainbow(10)

# set a specific channel
set_channel(spectrum, 'r', c(10, 50))
set_channel(spectrum, 'l', 50, space = 'lab')
set_channel(spectrum, 'alpha', c(0.5, 1))

# Add value to channel
add_to_channel(spectrum, 'r', c(10, 50))
add_to_channel(spectrum, 'l', 50, space = 'lab')

# Multiply a channel
multiply_channel(spectrum, 'r', c(10, 50))
multiply_channel(spectrum, 'l', 50, space = 'lab')

# set a lower bound on a channel
raise_channel(spectrum, 'r', c(10, 50))
raise_channel(spectrum, 'l', 20, space = 'lab')

# set an upper bound on a channel
cap_channel(spectrum, 'r', c(100, 50))
cap_channel(spectrum, 'l', 20, space = 'lab')