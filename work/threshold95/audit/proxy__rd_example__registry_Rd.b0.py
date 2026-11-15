import pandas as pd
import numpy as np
import textwrap

# Full proxy registry table: (folder, names_list, FUN, distance, PREFUN, convert, type, loop, C_FUN, formula)
_DEF = [
    ("Jaccard", ["Jaccard","binary","Reyssac","Roux"], "R_bjaccard", False, "pr_Jaccard_prefun", "pr_simil2dist", "binary", False, True, "a / (a + b + c)"),
    ("Kulczynski1", ["Kulczynski1"], "pr_Kulczynski1", False, None, "pr_simil2dist", "binary", True, False, "a / (b + c)"),
    ("Kulczynski2", ["Kulczynski2"], "pr_Kulczynski2", False, None, "pr_simil2dist", "binary", True, False, "[a / (a + b) + a / (a + c)] / 2"),
    ("Mountford", ["Mountford"], "pr_Mountford", False, None, "pr_simil2dist", "binary", True, False, "2a / (ab + ac + 2bc)"),
    ("Fager", ["Fager","McGowan"], "pr_fagerMcgowan", False, None, "pr_simil2dist", "binary", True, False, "a / sqrt((a + b)(a + c)) - sqrt(a + c) / 2"),
    ("Russel", ["Russel","Rao"], "pr_RusselRao", False, None, "pr_simil2dist", "binary", True, False, "a / n"),
    ("simple matching", ["simple matching","Sokal/Michener"], "pr_SimpleMatching", False, None, "pr_simil2dist", "binary", True, False, "(a + d) / n"),
    ("Hamman", ["Hamman"], "pr_Hamman", False, None, "pr_simil2dist", "binary", True, False, "([a + d] - [b + c]) / n"),
    ("Faith", ["Faith"], "pr_Faith", False, None, "pr_simil2dist", "binary", True, False, "(a + d/2) / n"),
    ("Tanimoto", ["Tanimoto","Rogers"], "pr_RogersTanimoto", False, None, "pr_simil2dist", "binary", True, False, "(a + d) / (a + 2b + 2c + d)"),
    ("Dice", ["Dice","Czekanowski","Sorensen"], "pr_Dice", False, None, "pr_simil2dist", "binary", True, False, "2a / (2a + b + c)"),
    ("Phi", ["Phi"], "pr_Phi", False, None, "pr_simil2dist", "binary", True, False, "(ad - bc) / sqrt[(a + b)(c + d)(a + c)(b + d)]"),
    ("Stiles", ["Stiles"], "pr_Stiles", False, None, "pr_simil2dist", "binary", True, False, "log(n(|ad-bc| - 0.5n)^2 / [(a + b)(c + d)(a + c)(b + d)])"),
    ("Michael", ["Michael"], "pr_Michael", False, None, "pr_simil2dist", "binary", True, False, "4(ad - bc) / [(a + d)^2 + (b + c)^2]"),
    ("Mozley", ["Mozley","Margalef"], "pr_MozleyMargalef", False, None, "pr_simil2dist", "binary", True, False, "an / (a + b)(a + c)"),
    ("Yule", ["Yule"], "pr_Yule", False, None, "pr_simil2dist", "binary", True, False, "(ad - bc) / (ad + bc)"),
    ("Yule2", ["Yule2"], "pr_Yule2", False, None, "pr_simil2dist", "binary", True, False, "(sqrt(ad) - sqrt(bc)) / (sqrt(ad) + sqrt(bc))"),
    ("Ochiai", ["Ochiai"], "pr_Ochiai", False, None, "pr_simil2dist", "binary", True, False, "a / sqrt[(a + b)(a + c)]"),
    ("Simpson", ["Simpson"], "pr_Simpson", False, None, "pr_simil2dist", "binary", True, False, "a / min{(a + b), (a + c)}"),
    ("Braun-Blanquet", ["Braun-Blanquet"], "pr_BraunBlanquet", False, None, "pr_simil2dist", "binary", True, False, "a / max{(a + b), (a + c)}"),
    ("cosine", ["cosine"], "R_cosine", False, "pr_cos_prefun", None, "metric", True, False, "xy / sqrt(xx * yy)"),
    ("angular", ["angular"], "pr_angular", False, None, None, "metric", True, False, "1 - acos(xy / sqrt(xx * yy)) / pi"),
    ("eJaccard", ["eJaccard","extended_Jaccard"], "pr_eJaccard", False, None, None, "metric", True, False, "xy / (xx + yy - xy)"),
    ("eDice", ["eDice","extended_Dice","eSorensen"], "pr_eDice", False, None, None, "metric", True, False, "2xy / (xx + yy)"),
    ("correlation", ["correlation"], "pr_correlation", False, None, None, "metric", True, False, "xy / sqrt(xx * yy) for centered x,y"),
    ("Chi-squared", ["Chi-squared"], "pr_ChiSquared", False, None, None, "nominal", True, False, "sum_ij (o_i - e_i)^2 / e_i"),
    ("Phi-squared", ["Phi-squared"], "pr_PhiSquared", False, None, None, "nominal", True, False, "[sum_ij (o_i - e_i)^2 / e_i] / n"),
    ("Tschuprow", ["Tschuprow"], "pr_Tschuprow", False, None, None, "nominal", True, False, "sqrt{[sum_ij (o_i - e_i)^2 / e_i] / n / sqrt((p - 1)(q - 1))}"),
    ("Cramer", ["Cramer"], "pr_Cramer", False, None, None, "nominal", True, False, "sqrt{[Chi / n)] / min[(p - 1), (q - 1)]}"),
    ("Pearson", ["Pearson","contingency"], "pr_Pearson", False, None, None, "nominal", True, False, "sqrt{Chi / (n + Chi)}"),
    ("Gower", ["Gower"], "pr_Gower", False, None, None, "other", True, False, "Sum_k (s_ijk * w_k) / Sum_k (d_ijk * w_k)"),
    ("Euclidean", ["Euclidean","L2"], "pr_Euclidean", True, None, None, "metric", True, False, "sqrt(sum_i (x_i - y_i)^2))"),
    ("Mahalanobis", ["Mahalanobis"], "pr_Mahalanobis", True, None, None, "metric", True, False, "sqrt((x - y) Sigma^(-1) (x - y))"),
    ("Bhjattacharyya", ["Bhjattacharyya"], "pr_Bhjattacharyya", True, None, None, "metric", True, False, "sqrt(sum_i (sqrt(x_i) - sqrt(y_i))^2))"),
    ("Manhattan", ["Manhattan","City-Block","L1","taxi"], "pr_Manhattan", True, None, None, "metric", True, False, "sum_i |x_i - y_i|"),
    ("supremum", ["supremum","max","maximum","Tschebyscheff","Chebyshev"], "pr_supremum", True, None, None, "metric", True, False, "max_i |x_i - y_i|"),
    ("Minkowski", ["Minkowski","Lp"], "pr_Minkowski", True, None, None, "metric", True, False, "(sum_i (x_i - y_i)^p)^(1/p)"),
    ("Canberra", ["Canberra"], "pr_Canberra", True, None, None, "metric", True, False, "sum_i |x_i - y_i| / |x_i + y_i|"),
    ("Wave", ["Wave","Hedges"], "pr_Wave", True, None, None, "metric", True, False, "sum_i (1 - min(x_i, y_i) / max(x_i, y_i))"),
    ("divergence", ["divergence"], "pr_divergence", True, None, None, "metric", True, False, "sum_i (x_i - y_i)^2 / (x_i + y_i)^2"),
    ("Kullback", ["Kullback","Leibler"], "pr_Kullback", True, None, None, "metric", True, False, "sum_i [x_i * log((x_i / sum_j x_j) / (y_i / sum_j y_j)) / sum_j x_j)]"),
    ("Bray", ["Bray","Curtis"], "pr_Bray", True, None, None, "metric", True, False, "sum_i |x_i - y_i| / sum_i (x_i + y_i)"),
    ("Soergel", ["Soergel"], "pr_Soergel", True, None, None, "metric", True, False, "sum_i |x_i - y_i| / sum_i max{x_i, y_i}"),
    ("Levenshtein", ["Levenshtein"], "pr_Levenshtein", True, None, None, "other", True, False, "Number of insertions, edits, and deletions between to strings"),
    ("Podani", ["Podani","discordance"], "pr_Podani", True, None, None, "metric", True, False, "1 - 2 * (a - b + c - d) / (n * (n - 1))"),
    ("Chord", ["Chord"], "pr_Chord", True, None, None, "metric", True, False, "sqrt(2 * (1 - xy / sqrt(xx * yy)))"),
    ("Geodesic", ["Geodesic"], "pr_Geodesic", True, None, None, "metric", True, False, "arccos(xy / sqrt(xx * yy))"),
    ("Whittaker", ["Whittaker"], "pr_Whittaker", True, None, None, "metric", True, False, "sum_i |x_i / sum_i x - y_i / sum_i y| / 2"),
    ("Hellinger", ["Hellinger"], "pr_Hellinger", True, None, None, "metric", True, False, "sqrt(sum_i (sqrt(x_i / sum_i x) - sqrt(y_i / sum_i y)) ^ 2)"),
    ("fJaccard", ["fJaccard","fuzzy_Jaccard"], "pr_fJaccard", True, None, None, "metric", True, False, "sum_i (min{x_i, y_i} / max{x_i, y_i})"),
]


def _strwrap(s, width=60):
    out = textwrap.wrap(s, width=width, break_long_words=False, break_on_hyphens=False)
    return out if out else [""]


class ProxyDB:
    def __init__(self):
        self._fields = [
            "names", "FUN", "distance", "PREFUN", "POSTFUN", "convert",
            "type", "loop", "C_FUN", "PACKAGE", "abcd", "formula",
            "reference", "description"
        ]
        self._entries = {}
        self._populate_defaults()

    def _populate_defaults(self):
        for folder, names_list, FUN, distance, PREFUN, convert, typ, loop, C_FUN, formula in _DEF:
            entry = {f: None for f in self._fields}
            entry.update({
                "names": ", ".join(names_list),
                "FUN": FUN,
                "distance": distance,
                "PREFUN": PREFUN,
                "convert": convert,
                "type": typ,
                "loop": loop,
                "C_FUN": C_FUN,
                "PACKAGE": "proxy",
                "abcd": False,
                "formula": formula,
            })
            if folder == "Jaccard":
                entry["reference"] = "Jaccard, P. (1908). Nouvelles recherches sur la distribution florale. Bull. Soc. Vaud. Sci. Nat., 44, pp. 223--270."
                entry["description"] = "The Jaccard Similarity (C implementation) for binary data. It is the proportion of (TRUE, TRUE) pairs, but not considering (FALSE, FALSE) pairs. So it compares the intersection with the union of object sets."
            self._entries[folder] = entry

# r2py:entity:pr_DB$set_entry
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

# r2py:entity:pr_DB$get_entry
    def get_entry(self, name):
        search_name = name.lower()
        for k, v in self._entries.items():
            if k.lower() == search_name:
                return v
        return None

# r2py:entity:pr_DB$modify_entry
    def modify_entry(self, names, description):
        for k in self._entries:
            if k.lower() == names.lower():
                self._entries[k]["description"] = description
                break

# r2py:entity:pr_DB$set_field
    def set_field(self, field_name):
        if field_name not in self._fields:
            self._fields.append(field_name)
            for entry in self._entries.values():
                entry[field_name] = None

# r2py:entity:pr_DB$get_entries
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

# r2py:entity:length
    def __len__(self):
        return len({id(v) for v in self._entries.values()})

    def __getitem__(self, key):
        return self.get_entry(key)

# r2py:entity:summary
    def summary(self, mode="long"):
        sim = []
        dist = []
        seen_ids = set()
        for name, v in self._entries.items():
            if id(v) in seen_ids:
                continue
            seen_ids.add(id(v))
            disp_name = str(v.get("names", name)).replace(", ", "/")
            f_val = v.get("formula") or "NA"
            t_val = v.get("type") or "other"
            line = f"     {disp_name} ({t_val}) = {f_val}"
            if v.get("distance"):
                dist.append(line)
            else:
                sim.append(line)
        out = ["* Similarity measures:"] + sim
        out.append("")
        out.append("* Distance measures:") if dist else None
        out.extend(dist)
        return "\n".join(out)

# r2py:entity:pr_DB$delete_entry
    def delete_entry(self, name):
        target_obj = self.get_entry(name)
        if target_obj:
            keys_to_del = [k for k, v in self._entries.items() if v is target_obj]
            for k in keys_to_del:
                del self._entries[k]

# r2py:entity:pr_DB$entry_exists
    def entry_exists(self, name):
        return any(k.lower() == name.lower() for k in self._entries)

# r2py:entity:as.data.frame
    def df_columns(self):
        uniq = self.get_entries()
        rownames = list(uniq.keys())
        cols = [f for f in self._fields if f != "names"]
        cols_data = []
        for c in cols:
            col = []
            for v in uniq.values():
                col.append(r_format_cell(v.get(c)))
            cols_data.append(col)
        return cols, cols_data, rownames


def r_format_cell(val):
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if val is None:
        return "<NA>"
    if callable(val):
        return getattr(val, "__r_deparse__", "function () NULL")
    return str(val)


def print_dataframe(colnames, cols_data, rownames, width=80):
    ncol = len(colnames)
    colwidths = []
    for j in range(ncol):
        mx = max((len(x) for x in cols_data[j]), default=0)
        colwidths.append(max(len(colnames[j]), mx))
    rownw = max((len(r) for r in rownames), default=0)

    blocks = []
    block = []
    cur = rownw
    for j in range(ncol):
        if block and cur + 1 + colwidths[j] > width:
            blocks.append(block)
            block = []
            cur = rownw
        block.append(j)
        cur += 1 + colwidths[j]
    blocks.append(block)

    lines = []
    for blk in blocks:
        hdr = " " * rownw
        for j in blk:
            hdr += " " + colnames[j].rjust(colwidths[j])
        lines.append(hdr)
        for i in range(len(rownames)):
            row = rownames[i].ljust(rownw)
            for j in blk:
                row += " " + cols_data[j][i].rjust(colwidths[j])
            lines.append(row)
    for ln in lines:
        print(ln)


def r_print_entry(entry):
    if entry is None:
        return
    fields = pr_DB._fields
    w = max(len(f) for f in fields)
    for field in fields:
        val = entry.get(field)
        if isinstance(val, bool):
            sval = "TRUE" if val else "FALSE"
            wrapped = [sval]
        elif val is None:
            wrapped = ["NA"]
        elif callable(val):
            wrapped = [getattr(val, "__r_deparse__", "function () NULL")]
        else:
            wrapped = _strwrap(str(val), 60)
        for i, line in enumerate(wrapped):
            if i == 0:
                print(field.rjust(w) + " " + line)
            else:
                print(" " * (w + 1) + line)


def r_print_entry_list(mapping):
    first = True
    for k, v in mapping.items():
        if not first:
            print("")
        first = False
        print("$" + k)
        r_print_entry(v)


pr_DB = ProxyDB()

# r2py:entity:mydist
def mydist(x, y):
    return x * y
mydist.__r_deparse__ = "function (x, y) x * y"

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
# r2py:entity:length
r_print_entry(pr_DB["test"])
print(f"[1] {len(pr_DB)}")

# r2py:entity:pr_DB$get_entries
entries_foo = pr_DB.get_entries(pattern="foo")
r_print_entry_list(entries_foo)

# r2py:entity:summary
print(pr_DB.summary("long"))

# r2py:entity:pr_DB$get_entries_1
all_entries = pr_DB.get_entries()
keys = list(all_entries.keys())
first_two = {k: all_entries[k] for k in keys[:2]}
r_print_entry_list(first_two)

# r2py:entity:as.data.frame
_colnames, _cols_data, _rownames = pr_DB.df_columns()
print_dataframe(_colnames[0:3], _cols_data[0:3], _rownames)

# r2py:entity:pr_DB$delete_entry
pr_DB.delete_entry("test")
# r2py:entity:pr_DB$entry_exists
print(f"[1] {str(pr_DB.entry_exists('test')).upper()}")