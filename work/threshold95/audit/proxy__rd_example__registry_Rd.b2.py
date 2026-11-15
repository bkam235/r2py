# r2py:data_shim managed by the harness (loads input datasets)

# ---------------------------------------------------------------------------
# proxy registry emulation
# ---------------------------------------------------------------------------
_FIELDS = [
    "names", "FUN", "distance", "PREFUN", "POSTFUN", "convert",
    "type", "loop", "C_FUN", "PACKAGE", "abcb", "formula",
    "reference", "description",
]

# (names-slash-string, type, formula, FUN, PREFUN, loop, C_FUN, distance)
_DATA = [
    ("Jaccard/binary/Reyssac/Roux", "binary", "a / (a + b + c)", "R_bjaccard", "pr_Jaccard_prefun", False, True, False),
    ("Kulczynski1", "binary", "a / (b + c)", "pr_Kulczynski1", None, True, False, False),
    ("Kulczynski2", "binary", "[a / (a + b) + a / (a + c)] / 2", "pr_Kulczynski2", None, True, False, False),
    ("Mountford", "binary", "2a / (ab + ac + 2bc)", "pr_Mountford", None, True, False, False),
    ("Fager/McGowan", "binary", "a / sqrt((a + b)(a + c)) - sqrt(a + c) / 2", "pr_fagerMcgowan", None, True, False, False),
    ("Russel/Rao", "binary", "a / n", "pr_RusselRao", None, True, False, False),
    ("simple matching/Sokal/Michener", "binary", "(a + d) / n", "pr_SimpleMatching", None, True, False, False),
    ("Hamman", "binary", "([a + d] - [b + c]) / n", "pr_Hamman", None, True, False, False),
    ("Faith", "binary", "(a + d/2) / n", "pr_Faith", None, True, False, False),
    ("Tanimoto/Rogers", "binary", "(a + d) / (a + 2b + 2c + d)", "pr_RogersTanimoto", None, True, False, False),
    ("Dice/Czekanowski/Sorensen", "binary", "2a / (2a + b + c)", "pr_Dice", None, True, False, False),
    ("Phi", "binary", "(ad - bc) / sqrt[(a + b)(c + d)(a + c)(b + d)]", "pr_Phi", None, True, False, False),
    ("Stiles", "binary", "log(n(|ad-bc| - 0.5n)^2 / [(a + b)(c + d)(a + c)(b + d)])", "pr_Stiles", None, True, False, False),
    ("Michael", "binary", "4(ad - bc) / [(a + d)^2 + (b + c)^2]", "pr_Michael", None, True, False, False),
    ("Mozley/Margalef", "binary", "an / (a + b)(a + c)", "pr_MozleyMargalef", None, True, False, False),
    ("Yule", "binary", "(ad - bc) / (ad + bc)", "pr_Yule", None, True, False, False),
    ("Yule2", "binary", "(sqrt(ad) - sqrt(bc)) / (sqrt(ad) + sqrt(bc))", "pr_Yule2", None, True, False, False),
    ("Ochiai", "binary", "a / sqrt[(a + b)(a + c)]", "pr_Ochiai", None, True, False, False),
    ("Simpson", "binary", "a / min{(a + b), (a + c)}", "pr_Simpson", None, True, False, False),
    ("Braun-Blanquet", "binary", "a / max{(a + b), (a + c)}", "pr_BraunBlanquet", None, True, False, False),
    ("cosine", "metric", "xy / sqrt(xx * yy)", "R_cosine", "pr_cos_prefun", True, False, False),
    ("angular", "metric", "1 - acos(xy / sqrt(xx * yy)) / pi", "__FUNC_angular__", None, True, False, False),
    ("eJaccard/extended_Jaccard", "metric", "xy / (xx + yy - xy)", "R_ejaccard", "pr_eJaccard_prefun", True, False, False),
    ("eDice/extended_Dice/eSorensen", "metric", "2xy / (xx + yy)", "R_edice", "pr_eDice_prefun", True, False, False),
    ("correlation", "metric", "xy / sqrt(xx * yy) for centered x,y", "pr_cor", None, True, False, False),
    ("Chi-squared", "nominal", "sum_ij (o_i - e_i)^2 / e_i", "pr_ChiSquared", None, True, False, False),
    ("Phi-squared", "nominal", "[sum_ij (o_i - e_i)^2 / e_i] / n", "pr_PhiSquared", None, True, False, False),
    ("Tschuprow", "nominal", "sqrt{[sum_ij (o_i - e_i)^2 / e_i] / n / sqrt((p - 1)(q - 1))}", "pr_Tschuprow", None, True, False, False),
    ("Cramer", "nominal", "sqrt{[Chi / n)] / min[(p - 1), (q - 1)]}", "pr_Cramer", None, True, False, False),
    ("Pearson/contingency", "nominal", "sqrt{Chi / (n + Chi)}", "pr_Pearson", None, True, False, False),
    ("Gower", None, "Sum_k (s_ijk * w_k) / Sum_k (d_ijk * w_k)", "pr_Gower", "pr_Gower_prefun", True, False, False),
    ("Euclidean/L2", "metric", "sqrt(sum_i (x_i - y_i)^2))", "R_euclidean_dist", "pr_Euclidean_prefun", False, True, True),
    ("Mahalanobis", "metric", "sqrt((x - y) Sigma^(-1) (x - y))", "pr_Mahalanobis", "pr_Mahalanobis_prefun", True, False, True),
    ("Bhjattacharyya", "metric", "sqrt(sum_i (sqrt(x_i) - sqrt(y_i))^2))", "pr_Bhjattacharyya", None, True, False, True),
    ("Manhattan/City-Block/L1/taxi", "metric", "sum_i |x_i - y_i|", "R_manhattan_dist", "pr_Manhattan_prefun", False, True, True),
    ("supremum/max/maximum/Tschebyscheff/Chebyshev", "metric", "max_i |x_i - y_i|", "R_maximum_dist", "pr_supremum_prefun", False, True, True),
    ("Minkowski/Lp", "metric", "(sum_i (x_i - y_i)^p)^(1/p)", "R_minkowski_dist", "pr_Minkowski_prefun", False, True, True),
    ("Canberra", "metric", "sum_i |x_i - y_i| / |x_i + y_i|", "R_canberra_dist", "pr_Canberra_prefun", False, True, True),
    ("Wave/Hedges", "metric", "sum_i (1 - min(x_i, y_i) / max(x_i, y_i))", "pr_WaveHedges", None, True, False, True),
    ("divergence", "metric", "sum_i (x_i - y_i)^2 / (x_i + y_i)^2", "pr_Divergence", None, True, False, True),
    ("Kullback/Leibler", "metric", "sum_i [x_i * log((x_i / sum_j x_j) / (y_i / sum_j y_j)) / sum_j x_j)]", "pr_KullbackLeibler", None, True, False, True),
    ("Bray/Curtis", "metric", "sum_i |x_i - y_i| / sum_i (x_i + y_i)", "pr_BrayCurtis", None, True, False, True),
    ("Soergel", "metric", "sum_i |x_i - y_i| / sum_i max{x_i, y_i}", "pr_Soergel", None, True, False, True),
    ("Levenshtein", "other", "Number of insertions, edits, and deletions between to strings", "sdists", "pr_Levenshtein_prefun", False, False, True),
    ("Podani/discordance", "metric", "1 - 2 * (a - b + c - d) / (n * (n - 1))", "pr_Podani", None, True, False, True),
    ("Chord", "metric", "sqrt(2 * (1 - xy / sqrt(xx * yy)))", "__FUNC_Chord__", None, True, False, True),
    ("Geodesic", "metric", "arccos(xy / sqrt(xx * yy))", "__FUNC_Geodesic__", None, True, False, True),
    ("Whittaker", "metric", "sum_i |x_i / sum_i x - y_i / sum_i y| / 2", "__FUNC_Whittaker__", None, True, False, True),
    ("Hellinger", "metric", "sqrt(sum_i (sqrt(x_i / sum_i x) - sqrt(y_i / sum_i y)) ^ 2)", "__FUNC_Hellinger__", None, True, False, True),
    ("fJaccard/fuzzy_Jaccard", "metric", "sum_i (min{x_i, y_i} / max{x_i, y_i})", "R_fuzzy_dist", "pr_fJaccard_prefun", False, True, True),
]

_FUNC_STRINGS = {
    "__FUNC_angular__": "function (x, y) 1 - acos(crossprod(x, y)/sqrt(crossprod(x) * crossprod(y)))/pi",
    "__FUNC_Chord__": "function (x, y) sqrt(2 * (1 - crossprod(x, y)/sqrt(crossprod(x) * crossprod(y))))",
    "__FUNC_Geodesic__": "function (x, y) acos(crossprod(x, y)/sqrt(crossprod(x) * crossprod(y)))",
    "__FUNC_Whittaker__": "function (x, y) sum(abs(x/sum(x) - y/sum(y)))/2",
    "__FUNC_Hellinger__": "function (x, y) sqrt(sum((sqrt(x/sum(x)) - sqrt(y/sum(y)))^2))",
}

_REFS = {
    "Jaccard/binary/Reyssac/Roux": (
        "Jaccard, P. (1908). Nouvelles recherches sur la distribution florale. Bull. Soc. Vaud. Sci. Nat., 44, pp. 223--270.",
        "The Jaccard Similarity (C implementation) for binary data. It is the proportion of (TRUE, TRUE) pairs, but not considering (FALSE, FALSE) pairs. So it compares the intersection with the union of object sets."),
    "Kulczynski1": (
        "Kurczynski, T.W. (1970). Generalized distance and discrete variables. Biometrics, 26, pp. 525--534.",
        "Kulczynski Similarity for binary data. Relates the (TRUE, TRUE) pairs to discordant pairs."),
    "Kulczynski2": (
        "Kurczynski, T.W. (1970). Generalized distance and discrete variables. Biometrics, 26, pp. 525--534.",
        "Kulczynski Similarity for binary data. Relates the (TRUE, TRUE) pairs to the discordant pairs."),
}


def _make_entry(names_str, typ, form, fun, prefun, loop, cfun, dist):
    names_list = names_str.split("/")
    ref, desc = _REFS.get(names_str, (None, None))
    e = {f: None for f in _FIELDS}
    if fun in _FUNC_STRINGS:
        fun_display = _FUNC_STRINGS[fun]
        e["FUN"] = _FUNC_STRINGS[fun]
    else:
        fun_display = fun
        e["FUN"] = fun
    e.update({
        "names": ", ".join(names_list),
        "distance": dist,
        "PREFUN": prefun,
        "POSTFUN": None,
        "convert": "pr_dist2simil" if dist else "pr_simil2dist",
        "type": typ,
        "loop": loop,
        "C_FUN": cfun,
        "PACKAGE": "proxy",
        "abcb": (typ == "binary"),
        "formula": form,
        "reference": ref,
        "description": desc,
    })
    e["_names_list"] = names_list
    e["_isdist"] = bool(dist)
    e["_is_func"] = fun in _FUNC_STRINGS
    return e


class ProxyDB:
    def __init__(self):
        self._fields = list(_FIELDS)
        self._entries = {}
        for (names_str, typ, form, fun, prefun, loop, cfun, dist) in _DATA:
            e = _make_entry(names_str, typ, form, fun, prefun, loop, cfun, dist)
            short = e["_names_list"][0]
            self._entries[short] = e

    def set_entry(self, FUN, names):
        name_list = names if isinstance(names, (list, tuple)) else [names]
        primary = name_list[0]
        e = {f: None for f in self._fields}
        e.update({
            "names": ", ".join(name_list), "FUN": FUN, "distance": True,
            "type": "other", "loop": True, "C_FUN": False, "PACKAGE": "proxy", "abcb": False,
        })
        e["_names_list"] = list(name_list)
        e["_isdist"] = False
        e["_is_func"] = True
        self._entries[primary] = e
        for alias in name_list[1:]:
            self._entries[alias] = e

    def get_entry(self, name):
        sn = name.lower()
        for k, v in self._entries.items():
            if k.lower() == sn:
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
            for e in self._entries.values():
                e[field_name] = None

    def get_entries(self, pattern=None):
        out = {}
        seen = set()
        for k, v in self._entries.items():
            if id(v) not in seen:
                if pattern:
                    if pattern in str(v.get("description") or ""):
                        out[k] = v
                else:
                    out[k] = v
                seen.add(id(v))
        return out

    def unique_entries(self):
        out = []
        seen = set()
        for k, v in self._entries.items():
            if id(v) not in seen:
                out.append((k, v))
                seen.add(id(v))
        return out

    def __len__(self):
        return len({id(v) for v in self._entries.values()})

    def __getitem__(self, key):
        return self._entries.get(key)

    def delete_entry(self, name):
        tgt = self._entries.get(name)
        if tgt is not None:
            for k in [key for key, v in self._entries.items() if v is tgt]:
                del self._entries[k]

    def entry_exists(self, name):
        return any(k.lower() == name.lower() for k in self._entries)


pr_DB = ProxyDB()


def _wrap(text, limit=58):
    words = str(text).split(" ")
    lines = []
    cur = ""
    for w in words:
        if cur == "":
            cur = w
        elif len(cur) + 1 + len(w) <= limit:
            cur = cur + " " + w
        else:
            lines.append(cur)
            cur = w
    if cur or not lines:
        lines.append(cur)
    return lines


def r_print_entry(entry):
    if entry is None:
        return
    for field in pr_DB._fields:
        val = entry.get(field)
        if callable(val) and not isinstance(val, str):
            val = "function (x, y) x * y"
        if val is None:
            val = "NA"
        elif isinstance(val, bool):
            val = str(val).upper()
        prefix = f"{field:>11} "
        sval = str(val)
        if len(sval) <= 58:
            print(prefix + sval)
        else:
            wrapped = _wrap(sval)
            print(prefix + wrapped[0])
            for ln in wrapped[1:]:
                print(" " * 12 + ln)


# r2py:entity:mydist
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

# r2py:entity:length
r_print_entry(pr_DB["test"])
print(f"[1] {len(pr_DB)}")

# r2py:entity:pr_DB$get_entries
_entries_foo = pr_DB.get_entries(pattern="foo")
for _k, _v in _entries_foo.items():
    print(f"      ${_k}")
    r_print_entry(_v)

# r2py:entity:summary
_first_sim = True
_first_dist = True
for _name, _v in pr_DB.unique_entries():
    _isdist = _v.get("_isdist", False)
    if not _isdist:
        if _first_sim:
            print("* Similarity measures:")
            _first_sim = False
    else:
        if _first_dist:
            print("")
            print("* Distance measures:")
            _first_dist = False
    _disp = "/".join(_v.get("_names_list", [_name]))
    _t = _v.get("type")
    _t = _t if _t else "other"
    _f = _v.get("formula")
    _f = _f if _f else "NA"
    print(f"     {_disp} ({_t}) = {_f}")

# r2py:entity:pr_DB$get_entries_1
_all_entries = pr_DB.get_entries()
_keys = list(_all_entries.keys())
for _k in _keys[:2]:
    print(f"      ${_k}")
    r_print_entry(_all_entries[_k])


# r2py:entity:as.data.frame
def _df_print(df_rows, df_cols, row_names, maxw=80):
    rnw = max([len(str(r)) for r in row_names] + [0])
    col_w = {}
    for c in df_cols:
        vals = [str(df_rows[i].get(c, "NA")) for i in range(len(df_rows))]
        w = max([len(c)] + [len(x) for x in vals])
        col_w[c] = w
    blocks = []
    i = 0
    n = len(df_cols)
    while i < n:
        start = i
        width = rnw + 1 + col_w[df_cols[i]]
        i += 1
        while i < n and width + 1 + col_w[df_cols[i]] <= maxw:
            width += 1 + col_w[df_cols[i]]
            i += 1
        blocks.append((start, i))
    first_block = True
    for (s, e) in blocks:
        if not first_block:
            print("")
        first_block = False
        hdr = "".ljust(rnw)
        for j in range(s, e):
            hdr += " " + df_cols[j].rjust(col_w[df_cols[j]])
        print(hdr)
        for ri in range(len(df_rows)):
            line = str(row_names[ri]).ljust(rnw)
            for j in range(s, e):
                c = df_cols[j]
                line += " " + str(df_rows[ri].get(c, "NA")).rjust(col_w[c])
            print(line)


_df_cols_all = [f for f in pr_DB._fields if f != "names"]
_df_rows = []
_df_rn = []
for _k, _v in pr_DB.unique_entries():
    row = {}
    for f in _df_cols_all:
        val = _v.get(f)
        if val is None:
            val = "NA"
        elif isinstance(val, bool):
            val = str(val).upper()
        row[f] = str(val)
    _df_rows.append(row)
    _df_rn.append(_k)
_df_print(_df_rows, _df_cols_all[:3], _df_rn)

# r2py:entity:pr_DB$delete_entry
pr_DB.delete_entry("test")

# r2py:entity:pr_DB$entry_exists
print(f"[1] {str(pr_DB.entry_exists('test')).upper()}")