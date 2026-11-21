# Translated from R by r2py
# r2py:data_shim managed by the harness (loads R's input data) - do not write it
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_felm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_felm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['airquality']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(broom)) -- no Python counterpart

# r2py:entity:import_broom
# library(broom) -- no Python equivalent; statsmodels is used below

# r2py:entity:is_installed
def _is_installed(pkg):
    try:
        __import__(pkg)
        return True
    except Exception:
        return False

is_installed = _is_installed("statsmodels")

# r2py:entity:import_lfe
# library(lfe) -- no Python equivalent; equivalent estimators below


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _fmt(v, digits=3):
    if v is None:
        return "NA"
    try:
        v = float(v)
    except Exception:
        return str(v)
    if np.isnan(v) or np.isinf(v):
        return "NA"
    if v == 0:
        return "0"
    a = abs(v)
    if a < 1e-10 or a >= 1e10:
        m, e = f"{v:.2e}".split("e")
        return f"{m}e{int(e):+03d}"
    e = int(np.floor(np.log10(a)))
    dec = max(0, digits - 1 - e)
    return f"{v:.{dec}f}"


def _fmt_int(v):
    if v is None:
        return "NA"
    try:
        v = float(v)
    except Exception:
        return "NA"
    if np.isnan(v):
        return "NA"
    return str(int(v))


def _mk_line(cells, widths, left):
    parts = []
    for j, c in enumerate(cells):
        c = str(c)
        parts.append(c.ljust(widths[j]) if j == left else c.rjust(widths[j]))
    return " ".join(parts).rstrip()


def _print_tibly(header, types, rows, left=0, max_rows=10):
    ncols = len(header)
    widths = []
    for j in range(ncols):
        cand = [len(str(header[j])), len(str(types[j]))]
        for r in rows:
            cand.append(len(str(r[j])))
        widths.append(max(cand))
    shown = rows if len(rows) <= max_rows else rows[:max_rows]
    pw = len(str(len(rows))) if rows else 1
    pad = " " * pw
    print(f"# A tibble: {len(rows)} × {ncols}")
    print(pad + " " + _mk_line(header, widths, left))
    print(pad + " " + _mk_line(types, widths, left))
    for i, r in enumerate(shown):
        print(f"{i + 1:<{pw}} " + _mk_line(r, widths, left))
    if len(rows) > max_rows:
        print(f"# ℹ {len(rows) - max_rows} more rows")


def _tidy_rows(beta, cov, terms, df):
    beta = np.asarray(beta, dtype=float)
    cov = np.asarray(cov, dtype=float)
    se = np.sqrt(np.diag(cov))
    tvals = beta / se
    pvals = 2 * st.t.sf(np.abs(tvals), df) if df is not None else 2 * st.norm.sf(np.abs(tvals))
    rows = []
    for i, tm in enumerate(terms):
        rows.append([tm, _fmt(beta[i]), _fmt(se[i]), _fmt(tvals[i]), _fmt(pvals[i])])
    return rows


def _tidy_with_ci(beta, cov, terms, df):
    beta = np.asarray(beta, dtype=float)
    cov = np.asarray(cov, dtype=float)
    se = np.sqrt(np.diag(cov))
    tvals = beta / se
    pvals = 2 * st.t.sf(np.abs(tvals), df)
    crit = float(st.t.isf(0.025, df))
    rows = []
    for i, tm in enumerate(terms):
        rows.append([
            tm, _fmt(beta[i]), _fmt(se[i]), _fmt(tvals[i]), _fmt(pvals[i]),
            _fmt(beta[i] - crit * se[i]), _fmt(beta[i] + crit * se[i]),
        ])
    return rows


# ---------------------------------------------------------------------------
# data (NA rows dropped exactly like R's model.frame)
# ---------------------------------------------------------------------------
d = airquality
_needed = ['Ozone', 'Temp', 'Wind', 'Solar.R']
_d = d.dropna(subset=_needed).copy()
_n = len(_d)
_rownames = [str(i + 1) for i in _d.index]
_y = _d['Ozone'].to_numpy(dtype=float)
_months = sorted(set(_d['Month'].to_numpy().tolist()))
_ym = _y - _y.mean()
_G_all = len(_months)

# ---------------------------------------------------------------------------
# head(airquality)
# ---------------------------------------------------------------------------
# r2py:entity:head
_h = airquality.head(6)
_hcols = list(_h.columns)
_hrows = []
for _j, _c in enumerate(_hcols):
    _vals = [_h[_c].iloc[_i] for _i in range(len(_h))]
    _nonna = [_v for _v in _vals if not pd.isna(_v)]
    _allint = all(float(_v) == int(float(_v)) for _v in _nonna) if _nonna else False
    if _allint:
        _strs = ["NA" if pd.isna(_v) else str(int(float(_v))) for _v in _vals]
    else:
        _dec = 0
        for _v in _nonna:
            _s = f"{float(_v):.10g}"
            _dec = max(_dec, len(_s.split('.')[1]) if '.' in _s else 0)
        _strs = ["NA" if pd.isna(_v) else f"{float(_v):.{_dec}f}" for _v in _vals]
    _hrows.append(_strs)
_rows_by_row = [[_hrows[_j][_i] for _j in range(len(_hcols))] for _i in range(len(_h))]
_hw = [max([len(_hcols[_j])] + [len(r[_j]) for r in _rows_by_row]) for _j in range(len(_hcols))]
print("  " + " ".join(_hcols[_j].rjust(_hw[_j]) for _j in range(len(_hcols))).rstrip())
for _i, _row in enumerate(_rows_by_row):
    print(f"{_i + 1} " + " ".join(_row[_j].rjust(_hw[_j]) for _j in range(len(_hcols))).rstrip())

# ---------------------------------------------------------------------------
# est0: felm(Ozone ~ Temp + Wind + Solar.R, airquality)
# ---------------------------------------------------------------------------
# r2py:entity:est0
_temp = _d['Temp'].to_numpy(dtype=float)
_wind = _d['Wind'].to_numpy(dtype=float)
_sol = _d['Solar.R'].to_numpy(dtype=float)
_X0 = np.column_stack([np.ones(_n), _temp, _wind, _sol])
_X0_df = pd.DataFrame(_X0, columns=['const', 'Temp', 'Wind', 'Solar.R'])
_m0 = sm.OLS(_y, _X0_df).fit()
_b0 = np.asarray(_m0.params, dtype=float)
_cov0 = np.asarray(_m0.cov_params(), dtype=float)
_inv0 = np.linalg.inv(_X0.T @ _X0)
_p0 = 4
_fitted0 = _X0 @ _b0
_resid0 = _y - _fitted0
_rss0 = float((_resid0 ** 2).sum())
_tss0 = float(((_y - _y.mean()) ** 2).sum())
_meat0 = (_X0 * _resid0[:, None]).T @ (_X0 * _resid0[:, None])
_robust0 = _inv0 @ _meat0 @ _inv0 * (_n / (_n - _p0))

est0 = {
    '__r2py_fp__': True,
    'class': ['felm'],
    'numbers': {
        'inv': [float(v) for v in _inv0.flatten(order='F')],
        'TSS': _tss0,
        'P.TSS': _tss0,
        'numctrl': 0,
        'beta': [float(v) for v in _b0],
        'coefficients': [float(v) for v in _b0],
        'Pp': 4,
        'N': int(_n),
        'p': 4,
        'residuals': [float(v) for v in _resid0],
        'c.fitted.values': [float(v) for v in _fitted0],
        'fitted.values': [float(v) for v in _fitted0],
        'r.residuals': [float(v) for v in _resid0],
        'vcv': [float(v) for v in _cov0.flatten(order='F')],
        'robustvcv': [float(v) for v in _robust0.flatten(order='F')],
    },
}

# r2py:entity:tidy
_t0_terms = ['(Intercept)', 'Temp', 'Wind', 'Solar.R']
_rows = _tidy_rows(_b0, _cov0, _t0_terms, _n - _p0)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# r2py:entity:augment
_a0 = []
for _i in range(_n):
    _a0.append([
        _rownames[_i], _fmt_int(_d['Ozone'].iloc[_i]), _fmt_int(_temp[_i]),
        _fmt(_wind[_i]), _fmt_int(_sol[_i]), _fmt(_fitted0[_i]), _fmt(_resid0[_i]),
    ])
_print_tibly(['.rownames', 'Ozone', 'Temp', 'Wind', 'Solar.R', '.fitted', '.resid'],
             ['<chr>', '<int>', '<int>', '<dbl>', '<int>', '<dbl>', '<dbl>'], _a0)

# ---------------------------------------------------------------------------
# est1: felm(Ozone ~ Temp + Wind + Solar.R | Month, airquality)
# ---------------------------------------------------------------------------
# r2py:entity:est1
_mo = _d['Month'].to_numpy()
_X1_df = pd.DataFrame({'Temp': _temp, 'Wind': _wind, 'Solar.R': _sol})
for _m in _months:
    _X1_df[f'Month.{_m}'] = (_mo == _m).astype(float)
_X1 = _X1_df.to_numpy(dtype=float)
_m1 = sm.OLS(_y, _X1_df).fit()
_b1 = np.asarray(_m1.params, dtype=float)
_K1 = _X1.shape[1]
_terms3 = ['Temp', 'Wind', 'Solar.R']
_loaded = list(_X1_df.columns)
_idks = [_loaded.index(t) for t in _terms3]
_b1_3 = _b1[_idks]
_p1 = _K1

_X3 = np.column_stack([_temp, _wind, _sol])
_Xdm = np.empty_like(_X3)
_ydm = np.empty_like(_y)
for _m in _months:
    _mk = _mo == _m
    _Xdm[_mk] = _X3[_mk] - _X3[_mk].mean(axis=0)
    _ydm[_mk] = _y[_mk] - _y[_mk].mean()
_inv3 = np.linalg.inv(_Xdm.T @ _Xdm)
_cfitted1 = _Xdm @ _b1_3
_fitted1 = _y - _ydm + _cfitted1
_resid1 = _y - _fitted1
_r_rsd = _y - _X3 @ _b1_3
_rss1 = float((_resid1 ** 2).sum())
_tss1 = float(((_y - _y.mean()) ** 2).sum())
_ptss1 = float((_ydm ** 2).sum())
_r2_1 = 1.0 - _rss1 / _tss1
_dm = _n - _p1
_vcv1 = _inv3 * (_rss1 / _dm)
_meat = (_Xdm * _resid1[:, None]).T @ (_Xdm * _resid1[:, None])
_robust1 = _inv3 @ _meat @ _inv3 * (_n / _dm)

est1 = {
    '__r2py_fp__': True,
    'class': ['felm'],
    'numbers': {
        'inv': [float(v) for v in _inv3.flatten(order='F')],
        'TSS': _tss1,
        'P.TSS': _ptss1,
        'numctrl': 0,
        'beta': [float(v) for v in _b1_3],
        'coefficients': [float(v) for v in _b1_3],
        'Pp': 3,
        'N': int(_n),
        'p': int(_p1),
        'residuals': [float(v) for v in _resid1],
        'c.fitted.values': [float(v) for v in _cfitted1],
        'fitted.values': [float(v) for v in _fitted1],
        'r.residuals': [float(v) for v in _r_rsd],
        'vcv': [float(v) for v in _vcv1.flatten(order='F')],
        'robustvcv': [float(v) for v in _robust1.flatten(order='F')],
    },
}

# r2py:entity:tidy_1
_rows = _tidy_rows(_b1_3, _vcv1, _terms3, _dm)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# r2py:entity:tidy_2
_se3 = np.sqrt(np.diag(_vcv1))
_sigma1 = np.sqrt(_rss1 / _dm)
_fe_rows = []
for _i, _tm in enumerate(_terms3):
    _t = _b1_3[_i] / _se3[_i]
    _fe_rows.append([_tm, _fmt(_b1_3[_i]), _fmt(_se3[_i]), _fmt(_t),
                     _fmt(2 * st.t.sf(abs(_t), _dm)), "NA", "NA"])
for _m in _months:
    _mk = _mo == _m
    _cnt = int(_mk.sum())
    _eff = float(np.mean(_r_rsd[_mk]))
    _sei = _sigma1 / np.sqrt(_cnt)
    _tv = _eff / _sei
    _pv = 2 * (1 - st.t.cdf(_tv, _cnt))
    _fe_rows.append([f'Month.{_m}', _fmt(_eff), _fmt(_sei), _fmt(_tv),
                     _fmt(_pv), str(_cnt), _fmt(1.0)])
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value', 'N', 'comp'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<int>', '<dbl>'], _fe_rows)

# r2py:entity:augment_1
_a1 = []
for _i in range(_n):
    _a1.append([
        _rownames[_i], _fmt_int(_d['Ozone'].iloc[_i]), _fmt_int(_temp[_i]),
        _fmt(_wind[_i]), _fmt_int(_sol[_i]), _fmt_int(_mo[_i]),
        _fmt(_fitted1[_i]), _fmt(_resid1[_i]),
    ])
_print_tibly(['.rownames', 'Ozone', 'Temp', 'Wind', 'Solar.R', 'Month', '.fitted', '.resid'],
             ['<chr>', '<int>', '<int>', '<dbl>', '<int>', '<int>', '<dbl>', '<dbl>'], _a1)

# r2py:entity:glance
_r2adj = 1.0 - (1.0 - _r2_1) * (_n - 1) / _dm
_sigma = np.sqrt(_rss1 / _dm)
_fstat = ((_tss1 - _rss1) / (_p1 - 1)) / (_rss1 / _dm)
_pf = float(st.f.sf(_fstat, _p1 - 1, _dm))
_print_tibly(['r.squared', 'adj.r.squared', 'sigma', 'statistic', 'p.value', 'df', 'df.residual', 'nobs'],
             ['<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<int>'],
             [[_fmt(_r2_1), _fmt(_r2adj), _fmt(_sigma), _fmt(float(_fstat)), _fmt(_pf),
               _fmt_int(_dm), _fmt_int(_dm), _fmt_int(_n)]])

# r2py:entity:tidy_3
_rows = _tidy_rows(_b1_3, _vcv1, _terms3, _dm)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# r2py:entity:tidy_4
_rows = _tidy_rows(_b1_3, _robust1, _terms3, _dm)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# ---------------------------------------------------------------------------
# est2: felm(Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month, airquality)
# ---------------------------------------------------------------------------
# r2py:entity:est2
# cluster vcov via full design (covariates + all month dummies)
_Xf = np.column_stack([_temp, _wind, _sol] + [(_mo == _m).astype(float) for _m in _months])
_Kf = _Xf.shape[1]
_bread = np.linalg.inv(_Xf.T @ _Xf)
_b_full = _bread @ (_Xf.T @ _y)
_u_full = _y - _Xf @ _b_full
_meat_cl = np.zeros((_Kf, _Kf))
for _m in _months:
    _mk = _mo == _m
    _s = _Xf[_mk].T @ _u_full[_mk]
    _meat_cl = _meat_cl + np.outer(_s, _s)
_G = _G_all
_Kfe = len(_months) - 1
_corr = (_G / (_G - 1)) * ((_n - 1) / (_n - _Kfe))
_V_full = _corr * (_bread @ _meat_cl @ _bread)
_cluster1 = _V_full[:3, :3]
_df2 = _G - 1

est2 = {
    '__r2py_fp__': True,
    'class': ['felm'],
    'numbers': {
        'inv': [float(v) for v in _inv3.flatten(order='F')],
        'TSS': _tss1,
        'P.TSS': _ptss1,
        'numctrl': 0,
        'beta': [float(v) for v in _b1_3],
        'coefficients': [float(v) for v in _b1_3],
        'Pp': 3,
        'N': int(_n),
        'p': int(_p1),
        'residuals': [float(v) for v in _resid1],
        'c.fitted.values': [float(v) for v in _cfitted1],
        'fitted.values': [float(v) for v in _fitted1],
        'r.residuals': [float(v) for v in _r_rsd],
        'vcv': [float(v) for v in _vcv1.flatten(order='F')],
        'robustvcv': [float(v) for v in _robust1.flatten(order='F')],
        'clustervcv': [float(v) for v in _cluster1.flatten(order='F')],
    },
}

# r2py:entity:tidy_5
_rows = _tidy_with_ci(_b1_3, _cluster1, _terms3, _df2)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value', 'conf.low', 'conf.high'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# r2py:entity:tidy_6
_rows = _tidy_with_ci(_b1_3, _cluster1, _terms3, _df2)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value', 'conf.low', 'conf.high'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# r2py:entity:tidy_7
_rows = _tidy_with_ci(_b1_3, _robust1, _terms3, _df2)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value', 'conf.low', 'conf.high'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)

# r2py:entity:tidy_8
_rows = _tidy_with_ci(_b1_3, _vcv1, _terms3, _df2)
_print_tibly(['term', 'estimate', 'std.error', 'statistic', 'p.value', 'conf.low', 'conf.high'],
             ['<chr>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>', '<dbl>'], _rows)