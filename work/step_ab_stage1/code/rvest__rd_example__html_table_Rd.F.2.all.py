import pandas as pd
from bs4 import BeautifulSoup
import io

# Helper to mimic R's minimal_html returning an xml_document-like object
class XMLDocument:
    def __init__(self, text):
        self.text = text

def minimal_html(html, title=""):
    # R's minimal_html produces a specific wrapper
    # We encapsulate the HTML in the same structure R does
    full_html = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>'
    return XMLDocument(full_html)

def html_element(x, css=None, xpath=None):
    # x is an XMLDocument, we need to parse it to search
    soup = BeautifulSoup(x.text, "html.parser")
    if css:
        return soup.select_one(css)
    if xpath:
        raise NotImplementedError("XPath not implemented in this translation.")
    return soup

def html_table(x, header=None, trim=True, dec=".", na_strings="NA", convert=True):
    # x is a BeautifulSoup element
    html_str = str(x)
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    # R's html_table behavior with colspan: pandas.read_html generally handles 
    # colspan by duplicating values, which matches rvest.
    
    if na_strings != "NA":
        df = df.replace(na_strings, pd.NA)
        
    if convert:
        # Try to convert to numeric. If it can be an integer, use Int64 (nullable)
        for col in df.columns:
            try:
                converted = pd.to_numeric(df[col], errors='coerce')
                # Check if all non-NaNs are integers
                if converted.dropna().mod(1).sum() == 0:
                    df[col] = converted.astype('Int64')
                else:
                    df[col] = converted
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
res1 = html_element(sample1, css="table")
res1 = html_table(res1)
print(res1.to_string(index=False))

# Values in merged cells will be duplicated
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
res2 = html_element(sample2, css="table")
res2 = html_table(res2)
print(res2.to_string(index=False))

# If a row is missing cells, they'll be filled with NAs
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
res3 = html_element(sample3, css="table")
res3 = html_table(res3)
print(res3.to_string(index=False))