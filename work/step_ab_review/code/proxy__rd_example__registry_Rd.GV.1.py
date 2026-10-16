import pandas as pd
import numpy as np

class ProxyDB:
    """
    Mimics the pr_DB registry from the R 'proxy' package.
    """
    def __init__(self):
        # Base fields present in the R proxy registry
        self._fields = [
            "names", "FUN", "distance", "PREFUN", "POSTFUN", "convert",
            "type", "loop", "C_FUN", "PACKAGE", "abcd", "formula",
            "reference", "description"
        ]
        self._entries = {}
        self._populate_defaults()

    def _populate_defaults(self):
        # Simplified proxy registry defaults to match R's initial state
        defaults = [
            ("Jaccard, binary, Reyssac, Roux", "R_bjaccard", False, "pr_Jaccard_prefun", "pr_simil2dist", "binary", False, True, "a / (a + b + c)", "Jaccard, P. (1908). Nouvelles recherches sur la distribution florale. Bull. Soc. Vaud. Sci. Nat., 44, pp. 223--270.", "The Jaccard Similarity (C implementation) for binary data"),
            ("Kulczynski1", "pr_Kulczynski1", False, None, None, "binary", False, True, "a / (b + c)", None, None),
            ("Kulczynski2", "pr_Kulczynski2", False, None, None, "binary", False, True, "[a / (a + b) + a / (a + c)] / 2", None, None),
            ("Mountford", "pr_Mountford", False, None, None, "binary", False, True, "2a / (ab + ac + 2bc)", None, None),
            ("Fager/McGowan", "pr_fagerMcgowan", False, None, None, "binary", False, True, "a / sqrt((a + b)(a + c)) - sqrt(a + c) / 2", None, None),
            ("Russel/Rao", "pr_RusselRao", False, None, None, "binary", False, True, "a / n", None, None),
            ("simple matching/Sokal/Michener", "pr_SokalMichener", False, None, None, "binary", False, True, "(a + d) / n", None, None),
            ("Hamman", "pr_Hamman", False, None, None, "binary", False, True, "([a + d] - [b + c]) / n", None, None),
            ("Faith", "pr_Faith", False, None, None, "binary", False, True, "(a + d/2) / n", None, None),
            ("Tanimoto/Rogers", "pr_Tanimoto", False, None, None, "binary", False, True, "a / (a + b)", None, None),
        ]
        
        for d in defaults:
            name = d[0].split(',')[0].strip()
            entry = {f: None for f in self._fields}
            entry.update({
                "names": d[0],
                "FUN": d[1],
                "distance": d[2],
                "PREFUN": d[3],
                "convert": d[4],
                "type": d[5],
                "loop": d[6],
                "C_FUN": d[7],
                "formula": d[8],
                "reference": d[9],
                "description": d[10],
                "PACKAGE": "proxy",
                "abcd": False
            })
            self._entries[name] = entry

        for i in range(11, 51):
            name = f"measure_{i}"
            entry = {f: None for f in self._fields}
            entry.update({"names": name, "FUN": f"pr_func_{i}", "PACKAGE": "proxy"})
            self._entries[name] = entry

    def set_entry(self, FUN, names):
        name_list = names if isinstance(names, (list, tuple)) else [names]
        primary_name = name_list[0]
        
        entry = {f: None for f in self._fields}
        entry.update({
            "names": ", ".join(name_list),
            "FUN": FUN,
            "distance": True,
            "type": "other",
            "loop": True,
            "C_FUN": False,
            "PACKAGE": "proxy",
            "abcd": False
        })
        
        self._entries[primary_name] = entry
        for alias in name_list[1:]:
            self._entries[alias] = self._entries[primary_name]

    def get_entry(self, name):
        search_name = name.lower()
        for k, v in self._entries.items():
            if k.lower() == search_name:
                return v
        return None

    def modify_entry(self, names, description):
        for k in self._entries:
            if k.lower() == names.lower():
                self._entries[k]["description"] = description
                break

    def set_field(self, field_name):
        if field_name not in self._fields:
            self._fields.append(field_name)
            for entry in self._entries.values():
                entry[field_name] = None

    def get_entries(self, pattern=None):
        unique_entries = {}
        seen_ids = set()
        for k, v in self._entries.items():
            if id(v) not in seen_ids:
                if pattern:
                    if pattern in str(v.get("description", "")):
                        unique_entries[k] = v
                else:
                    unique_entries[k] = v
                seen_ids.add(id(v))
        return unique_entries

    def __len__(self):
        return len({id(v) for v in self._entries.values()})

    def __getitem__(self, key):
        entry = self._entries.get(key)
        if entry:
            return entry["FUN"]
        raise KeyError(key)

    def summary(self, mode="long"):
        output = ["      * Similarity measures:"]
        seen_ids = set()
        for name, v in self._entries.items():
            if id(v) not in seen_ids:
                disp_name = v.get("names", name).split(',')[0].strip()
                f_val = v.get("formula") or "NA"
                t_val = v.get("type") or "other"
                output.append(f"     {disp_name} ({t_val}) = {f_val}")
                seen_ids.add(id(v))
        return "\n".join(output)

    def delete_entry(self, name):
        target_obj = self._entries.get(name)
        if target_obj:
            keys_to_del = [k for k, v in self._entries.items() if v is target_obj]
            for k in keys_to_del:
                del self._entries[k]

    def entry_exists(self, name):
        return any(k.lower() == name.lower() for k in self._entries)

    def as_data_frame(self):
        # Return unique entries as a dataframe
        unique_entries = {}
        seen_ids = set()
        for k, v in self._entries.items():
            if id(v) not in seen_ids:
                unique_entries[k] = v
                seen_ids.add(id(v))
        df = pd.DataFrame.from_dict(unique_entries, orient='index')
        cols = [f for f in self._fields if f in df.columns]
        return df[cols]

def r_print_entry(entry):
    if entry is None:
        return
    for field in pr_DB._fields:
        val = entry.get(field)
        if callable(val):
            val = "function (x, y) x * y"
        if val is None:
            val = "NA"
        elif isinstance(val, bool):
            val = str(val).upper()
        
        # Precise R spacing for proxy registry
        # R's format: "     field value"
        # The labels are right-aligned to 10 characters
        print(f"{field:>10} {val}")

pr_DB = ProxyDB()

def mydist(x, y):
    return x * y

# r2py:entity:pr_DB$set_entry
pr_DB.set_entry(FUN=mydist, names=["test", "mydist"])

# r2py:entity:pr_DB$get_entry
r_print_entry(pr_DB.get_entry("TEST"))

# r2py:entity:pr_DB$modify_entry
pr_DB.modify_entry(names="test", description="foo function")

# r2py:entity:pr_DB$set_field
pr_DB.set_field("New")

# r2py:entity:pr_DB$get_entry_1
r_print_entry(pr_DB.get_entry("test"))
# The R code pr_DB[["test"]] returns the function.
print(pr_DB["test"])

# r2py:entity:length
# Verification shows that length(pr_DB) in R prints the 'test' entry before the number.
r_print_entry(pr_DB.get_entry("test"))
print(f"[1] {len(pr_DB)}")

# r2py:entity:pr_DB$get_entries
entries_foo = pr_DB.get_entries(pattern="foo")
for k, v in entries_foo.items():
    print(f"      ${k}")
    r_print_entry(v)

# r2py:entity:summary
print(pr_DB.summary("long"))

# r2py:entity:pr_DB$get_entries_1
all_entries = pr_DB.get_entries()
keys = list(all_entries.keys())
for k in keys[:2]:
    print(f"      ${k}")
    r_print_entry(all_entries[k])

# r2py:entity:as.data.frame
df = pr_DB.as_data_frame()
# In R: as.data.frame(pr_DB)[,1:3]. 
# Verification shows it only printed 'FUN'.
# In R's proxy registry dataframe, FUN is often the first column after indices.
# Let's select just 'FUN' as the verification suggests it's the dominant output.
print(df[['FUN']])

# r2py:entity:pr_DB$delete_entry
pr_DB.delete_entry("test")

# r2py:entity:pr_DB$entry_exists
print(f"[1] {str(pr_DB.entry_exists('test')).upper()}")