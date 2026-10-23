# r2py crawler metadata
# package: pak
# source_type: rd_example
# topic: local_system_requirements.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pak\help
# lines: 15

suppressPackageStartupMessages(library(pak))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
local_system_requirements("ubuntu", "20.04")
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
pkg_system_requirements("pak", "ubuntu", "20.04")
pkg_system_requirements("pak", "redhat", "7")
pkg_system_requirements("config", "ubuntu", "20.04") # no sys reqs
pkg_system_requirements("curl", "ubuntu", "20.04")
pkg_system_requirements("git2r", "ubuntu", "20.04")
pkg_system_requirements(c("config", "git2r", "curl"), "ubuntu", "20.04")
# queried packages must exist
pkg_system_requirements("iDontExist", "ubuntu", "20.04")
pkg_system_requirements(c("curl", "iDontExist"), "ubuntu", "20.04")
}) # examplesIf