# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__vignette__broom_chunk6.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__vignette__broom_chunk6.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import math
from decimal import Decimal, ROUND_HALF_EVEN
import pandas as pd
import numpy as np
import statsmodels.api as sm


def _sig3(v):
    f = float(v)
    if math.isnan(f):
        return "NA"
    if f == 0:
        return "0"
    e = math.floor(math.log10(abs(f)))
    d = 2 - e
    q = Decimal(1).scaleb(-d)
    val = Decimal(repr(f)).quantize(q, rounding=ROUND_HALF_EVEN)
    return format(val, 'f')


def _print_tibble(df):
    names = list(df.columns)
    n = len(df)
    ncol = len(names)
    show = n
    if n > 10:
        show = 10 if ncol >= 5 else min(n, 20)
    footer = show < n
    types = []
    for c in names:
        s = str(df[c].dtype)
        if s.startswith('int') or s.startswith('bool'):
            types.append('int')
        elif s == 'object' or s.startswith('str'):
            types.append('chr')
        else:
            types.append('dbl')
    svals = []
    for j, c in enumerate(names):
        col = []
        if types[j] == 'int':
            for i in range(show):
                v = df.iloc[i, j]
                col.append('NA' if pd.isna(v) else str(int(v)))
        elif types[j] == 'chr':
            for i in range(show):
                col.append(str(df.iloc[i, j]))
        else:
            raw = [df.iloc[i, j] for i in range(show)]
            finite = [float(x) for x in raw if not pd.isna(x)]
            all_whole = len(finite) > 0 and all(abs(x - round(x)) < 1e-9 for x in finite)
            for x in raw:
                if pd.isna(x):
                    col.append('NA')
                elif all_whole:
                    col.append(str(int(round(float(x)))))
                else:
                    col.append(_sig3(x))
        svals.append(col)
    tmap = {'chr': '<chr>', 'dbl': '<dbl>', 'int': '<int>'}
    widths = []
    for j, c in enumerate(names):
        w = max(len(c), 5)
        for s in svals[j]:
            w = max(w, len(s))
        widths.append(w)
    rw = len(str(min(n, show)))
    print("# A tibble: %d \u00d7 %d" % (n, ncol))
    hdr = [' ' * rw]
    for j, c in enumerate(names):
        hdr.append(c.ljust(widths[j]) if types[j] == 'chr' else c.rjust(widths[j]))
    print(' '.join(hdr))
    typ = [' ' * rw]
    for j in range(ncol):
        t = tmap[types[j]]
        typ.append(t.ljust(widths[j]) if types[j] == 'chr' else t.rjust(widths[j]))
    print(' '.join(typ))
    for i in range(show):
        row = [str(i + 1).rjust(rw)]
        for j in range(ncol):
            cell = svals[j][i]
            row.append(cell.ljust(widths[j]) if types[j] == 'chr' else cell.rjust(widths[j]))
        print(' '.join(row))
    if footer:
        print("# \u2139 %d more rows" % (n - show))
        print("# \u2139 Use `print(n = ...)` to see more rows")


# suppressPackageStartupMessages(library(broom))
# r2py:entity:suppressPackageStartupMessages
# (broom not available in Python; no-op)

# r2py:entity:import_broom
# (broom library import - not available; using statsmodels instead)

df_mtcars = pd.DataFrame(mtcars)

# glmfit <- glm(am ~ wt, mtcars, family = "binomial")
# r2py:entity:glmfit
X = sm.add_constant(df_mtcars['wt'])
y = df_mtcars['am']
glmfit = sm.GLM(y, X, family=sm.families.Binomial()).fit()

# tidy(glmfit)
# r2py:entity:tidy
_terms = [('(Intercept)' if t == 'const' else t) for t in glmfit.params.index]
tidy = pd.DataFrame({
    'term': _terms,
    'estimate': np.asarray(glmfit.params),
    'std.error': np.asarray(glmfit.bse),
    'statistic': np.asarray(glmfit.tvalues),
    'p.value': np.asarray(glmfit.pvalues),
})
_print_tibble(tidy)

# augment(glmfit)
# r2py:entity:augment
_MTCARS_RN = [
    'Mazda RX4', 'Mazda RX4 Wag', 'Datsun 710', 'Hornet 4 Drive',
    'Hornet Sportabout', 'Valiant', 'Duster 360', 'Merc 240D', 'Merc 230',
    'Merc 280', 'Merc 280C', 'Merc 450SE', 'Merc 450SL', 'Merc 450SLC',
    'Cadillac Fleetwood', 'Lincoln Continental', 'Chrysler Imperial',
    'Fiat 128', 'Honda Civic', 'Toyota Corolla', 'Toyota Corona',
    'Dodge Challenger', 'AMC Javelin', 'Camaro Z28', 'Pontiac Firebird',
    'Fiat X1-9', 'Porsche 914-2', 'Lotus Europa', 'Ford Pantera L',
    'Ferrari Dino', 'Maserati Bora', 'Volvo 142E',
]
n_obs = int(glmfit.nobs)
influence = glmfit.get_influence()
_linpred = X.values.dot(np.asarray(glmfit.params))
_hat = np.asarray(influence.hat_matrix_diag)
_resid_dev = np.asarray(glmfit.resid_deviance)
_pearson = np.asarray(glmfit.resid_pearson)
augment = pd.DataFrame({
    '.rownames': _MTCARS_RN[:n_obs],
    'am': df_mtcars['am'].astype(float).values,
    'wt': df_mtcars['wt'].astype(float).values,
    '.fitted': _linpred,
    '.resid': _resid_dev,
    '.hat': _hat,
})
_dfres = float(glmfit.df_resid)
_chi2 = float(np.sum(_pearson ** 2))
_sigma = np.sqrt((_chi2 - _pearson ** 2 / (1 - _hat)) / (_dfres - 1))
augment['.sigma'] = _sigma
augment['.cooksd'] = np.asarray(influence.cooks_distance[0])
augment['.std.resid'] = _resid_dev / np.sqrt(1 - _hat)
_print_tibble(augment)

# glance(glmfit)
# r2py:entity:glance
llf = float(glmfit.llf)
_k = len(glmfit.params)
_bic = -2 * llf + np.log(n_obs) * _k
glance = pd.DataFrame({
    'null.deviance': [float(glmfit.null_deviance)],
    'df.null': [n_obs - 1],
    'logLik': [llf],
    'AIC': [float(glmfit.aic)],
    'BIC': [float(_bic)],
    'deviance': [float(glmfit.deviance)],
    'df.residual': [int(glmfit.df_resid)],
    'nobs': [n_obs],
})
_print_tibble(glance)