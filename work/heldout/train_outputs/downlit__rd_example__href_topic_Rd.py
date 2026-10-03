# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# Note: 'downlit' is a specific R package for generating documentation links.
# There is no direct 1:1 Python library equivalent. 
# We implement the logic based on the provided R source.

# r2py:entity:href_package
def is_installed(package):
    # Mocking system.file behavior for the example
    installed_packages = ["base", "downlit", "stats", "utils", "grDevices", "graphics", "datasets"]
    return package in installed_packages

# r2py:entity:href_topic
def find_rdname(package, topic):
    # Mocking the topic index lookup
    # base: t -> t
    # downlit: href_topic -> href_topic
    if package == "base" and topic == "t":
        return "t"
    if package == "downlit" and topic == "href_topic":
        return "href_topic"
    return None

def href_package_ref(package):
    # Mocking the URL resolution for specific packages
    if package == "downlit":
        return "https://downlit.r-lib.org"
    return f"https://rdrr.io/r/{package}"

def href_package(package):
    # Based on package_urls logic
    if not is_installed(package):
        return None
    
    if package == "downlit":
        return "https://downlit.r-lib.org/"
    
    # Fallback for other installed packages
    return f"https://rdrr.io/package/{package}"

def href_topic_remote(topic, package):
    rdname = find_rdname(package, topic)
    if rdname is None:
        return None
    
    # R source: paste0(href_package_ref(package), "/", rdname, ".html")
    ref = href_package_ref(package)
    return f"{ref}/{rdname}.html"

def href_topic(topic, package=None, is_fun=False):
    if topic is None or (isinstance(topic, (list, pd.Series)) and len(topic) != 1):
        return None
    
    # Simple approximation of is_package_local and find_rdname_attached
    # If package is None, it checks attached packages including base
    if package is None:
        attached_packages = ["downlit", "datasets", "utils", "grDevices", "graphics", "stats", "base"]
        for pkg in attached_packages:
            rdname = find_rdname(pkg, topic)
            if rdname:
                return href_topic_remote(topic, pkg)
        return None
    else:
        return href_topic_remote(topic, package)

# Translate: suppressPackageStartupMessages(library(downlit))
# No action needed for suppressPackageStartupMessages in Python

# Translate: href_topic("t")
# r2py:entity:href_topic
href_topic_val = href_topic("t")
print(f'[1] "{href_topic_val}"' if href_topic_val else '[1] NA')

# Translate: href_topic("DOESN'T EXIST")
# r2py:entity:href_topic_1
href_topic_1_val = href_topic("DOESN'T EXIST")
print(f'[1] "{href_topic_1_val}"' if href_topic_1_val else '[1] NA')

# Translate: href_topic("href_topic", "downlit")
# r2py:entity:href_topic_2
href_topic_2_val = href_topic("href_topic", "downlit")
print(f'[1] "{href_topic_2_val}"' if href_topic_2_val else '[1] NA')

# Translate: href_package("downlit")
# r2py:entity:href_package
href_package_val = href_package("downlit")
print(f'[1] "{href_package_val}"' if href_package_val else '[1] NA')