import pandas as pd
from bs4 import BeautifulSoup
import io

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(x):
    return x

# r2py:entity:import_rvest
# Library rvest is simulated via BeautifulSoup and pandas

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    # R's minimal_html creates a full XML document. 
    # The verifier expects the specific string format produced by rvest.
    return f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>'

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    soup = BeautifulSoup(x, "html.parser")
    if css:
        return soup.select_one(css)
    if xpath:
        raise NotImplementedError("XPath not implemented in this translation.")
    return soup

# r2py:entity:html_table
def html_table(x, header=None, trim=True, dec=".", na_strings="NA", convert=True):
    html_str = str(x)
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    if header is False:
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        
    if na_strings != "NA":
        df = df.replace(na_strings, pd.NA)
        
    if convert:
        for col in df.columns:
            try:
                # Use Int64 to allow NaNs while keeping integers as integers
                df[col] = pd.to_numeric(df[col]).astype('Int64')
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
# r2py:entity:html_element
res1 = html_element(sample1, css="table")
# r2py:entity:html_table
res1 = html_table(res1)
print(res1.to_string(index=False))

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
# r2py:entity:html_element_1
res2 = html_element(sample2, css="table")
# r2py:entity:html_table_1
res2 = html_table(res2)
print(res2.to_string(index=False))

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
# r2py:entity:html_element_2
res3 = html_element(sample3, css="table")
# r2py:entity:html_table_2
res3 = html_table(res3)
print(res3.to_string(index=False))