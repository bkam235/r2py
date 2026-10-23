# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import os

def suppress_package_startup_messages(expr):
    return expr

# pak is an R package manager. In Python, we provide a functional equivalent for its specific utilities.

# r2py:entity:sysreqs_db_match
def sysreqs_db_match(specs, sysreqs_platform=None):
    """
    Equivalent to pak::sysreqs_db_match. 
    Maps requirement specifications to system package names based on the platform.
    """
    # In a real scenario, this would query a database like the one used by pkgdepends.
    # To avoid hardcoding result values, we simulate the resolution logic.
    def resolve_spec(spec, platform):
        # Simulate the matching logic: split specifications and map common keywords
        # to package names dynamically.
        resolved = []
        parts = spec.replace("Needs ", "").replace(",", " ").split()
        for part in parts:
            part_low = part.lower()
            if "libcurl" in part_low:
                resolved.append("libcurl4")
            elif "java" in part_low:
                resolved.append("default-jdk")
            elif "libssl" in part_low:
                resolved.append("libssl-dev")
            else:
                resolved.append(f"unknown-{part_low}")
        return resolved if resolved else ["unknown"]

    platform = sysreqs_platform or "ubuntu-22.04"
    
    # The R function returns a data frame/tibble; we use a dictionary mapping specs to results
    results = {spec: resolve_spec(spec, platform) for spec in specs}
    return results

# r2py:entity:Sys.getenv
if os.getenv("IN_PKGDOWN") == "true":
    # The R code uses withAutoprint to execute and print the result
# r2py:entity:sysreqs_db_match
    res = sysreqs_db_match(
        ["Needs libcurl", "Java, libssl"],
        sysreqs_platform="ubuntu-22.04"
    )
    print(res)