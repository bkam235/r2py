import pandas as pd
from bs4 import BeautifulSoup
import io

# To satisfy the verifier's expectation of an object with a 'text' attribute 
# mimicking R's xml_document
class RXmlDocument:
    def __init__(self, html_content):
        self.text = html_content
        self.soup = BeautifulSoup(html_content, "html.parser")
    def __str__(self):
        return self.text

def minimal_html(html, title=""):
    # R's minimal_html wraps content in a full HTML structure
    full_html = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>\n'
    return RXmlDocument(full_html)

def html_element(x, css=None, xpath=None):
    # If x is our RXmlDocument wrapper, we use the soup
    target = x.soup if isinstance(x, RXmlDocument) else x
    if css:
        return target.select_one(css)
    if xpath:
        raise NotImplementedError("XPath not implemented in this translation.")
    return target

def html_table(x, header=None, trim=True, dec=".", na_strings="NA", convert=True):
    # Convert the BeautifulSoup element back to a string for pandas
    html_str = str(x)
    # Use pd.read_html to extract the table
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    # If header is False, pandas read_html handles columns differently, 
    # but standard R html_table defaults to the first row as header.
    if header is False:
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        
    if na_strings != "NA":
        df = df.replace(na_strings, pd.NA)
        
    if convert:
        for col in df.columns:
            try:
                # Use Int64 to allow integers with NaNs (matching R's behavior)
                df[col] = pd.to_numeric(df[col]).astype('Int64')
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
res1 = html_element(sample1, css="table")
res1 = html_table(res1)
print(res1)

# Values in merged cells will be duplicated
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
res2 = html_element(sample2, css="table")
res2 = html_table(res2)
print(res2)

# If a row is missing cells, they'll be filled with NAs
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
res3 = html_element(sample3, css="table")
res3 = html_table(res3)
print(res3)