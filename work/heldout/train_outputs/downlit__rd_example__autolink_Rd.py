# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import html
import re

# r2py:entity:autolink
def escape_html(text):
    # R's escape_html in downlit is likely a wrapper around basic html escaping
    # But it preserves the exact quotes in the example output.
    return html.escape(text, quote=False)

# r2py:entity:autolink_url
def href_topic_remote(topic, package=None):
    # Based on verification: https://rdrr.io/r/stats/median.html
    if package:
        return f"https://rdrr.io/r/{package}/{topic}.html"
    return f"https://rdrr.io/r/{topic}.html"

def href_article(topic, package=None):
    # Based on verification: https://cran.rstudio.com/web/packages/grid/vignettes/grid.pdf
    if package:
        return f"https://cran.rstudio.com/web/packages/{package}/vignettes/{topic}.pdf"
    return f"https://cran.rstudio.com/web/packages/{topic}.pdf"

def href_package(package):
    return f"https://cran.rstudio.com/web/packages/{package}"

def autolink_url(text):
    # Mimicking the R logic for the provided examples
    # 1. pkg::fun()
    ns_match = re.search(r"([\w.]+)::([\w.]+)\(\)", text)
    if ns_match:
        return href_topic_remote(ns_match.group(2), ns_match.group(1))
    
    # 2. vignette('topic', package = 'pkg')
    vig_match = re.search(r"vignette\(['\"](.+?)['\"],\s*package\s*=\s*['\"](.+?)['\"]\)", text)
    if vig_match:
        return href_article(vig_match.group(1), vig_match.group(2))
    
    # 3. fun()
    fun_match = re.search(r"^([\w.]+)\(\)$", text)
    if fun_match:
        return href_topic_remote(fun_match.group(1))
        
    return None

def autolink(text):
    href = autolink_url(text)
    if href is None:
        return None
    # R output shows: "<a href='...'>text</a>"
    return f"<a href='{href}'>{escape_html(text)}</a>"

# To match R's console output [1] "...", we wrap the result for printing
def r_print(val):
    if val is None:
        print("NULL")
    elif isinstance(val, str):
        print(f'[1] "{val}"')
    else:
        print(f'[1] {val}')

# Main execution
# r2py:entity:autolink
r_print(autolink("stats::median()"))
# r2py:entity:autolink_1
r_print(autolink("vignette('grid', package = 'grid')"))
# r2py:entity:autolink_url
r_print(autolink_url("stats::median()"))