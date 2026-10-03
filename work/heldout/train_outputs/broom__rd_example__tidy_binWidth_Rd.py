# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd
from scipy.stats import norm, beta

# r2py:entity:bw
def binWald(y, n, conf_level=0.95, alternative="two.sided"):
    alpha = 1 - conf_level
    est = y / n
    z1s = norm.ppf(conf_level)
    z2s = norm.ppf(1 - alpha / 2)
    if alternative == "two.sided":
        ki = [est - z2s * np.sqrt(est * (1 - est) / n), est + z2s * np.sqrt(est * (1 - est) / n)]
    elif alternative == "less":
        ki = [0, est + z1s * np.sqrt(est * (1 - est) / n)]
    elif alternative == "greater":
        ki = [est - z1s * np.sqrt(est * (1 - est) / n), 1]
    else:
        raise ValueError("alternative mis-specified")
    return ki

def binWilson(y, n, conf_level=0.95, alternative="two.sided"):
    alpha = 1 - conf_level
    t = y / n
    if alternative == "two.sided":
        z = norm.ppf(1 - alpha / 2)
        est_int = (y + (z**2) / 2) / (n + z**2)
        w_se = (z * np.sqrt(n * t * (1 - t) + (z**2) / 4)) / (n + z**2)
        ci = [est_int - w_se, est_int + w_se]
    elif alternative == "less":
        z = norm.ppf(1 - alpha)
        est_int = (y + (z**2) / 2) / (n + z**2)
        w_se = (z * np.sqrt(n * t * (1 - t) + (z**2) / 4)) / (n + z**2)
        ci = [0, est_int + w_se]
    elif alternative == "greater":
        z = norm.ppf(1 - alpha)
        est_int = (y + (z**2) / 2) / (n + z**2)
        w_se = (z * np.sqrt(n * t * (1 - t) + (z**2) / 4)) / (n + z**2)
        ci = [est_int - w_se, 1]
    else:
        raise ValueError("argument alternative misspecified")
    return ci

def binAC(y, n, conf_level=0.95, alternative="two.sided"):
    alpha = 1 - conf_level
    est = y / n
    z1s = norm.ppf(conf_level)
    z2s = norm.ppf(1 - alpha / 2)
    esti1s = (y + (z1s**2) / 2) / (n + z1s**2)
    esti2s = (y + (z2s**2) / 2) / (n + z2s**2)
    ni1s = n + z1s**2
    ni2s = n + z2s**2
    if alternative == "two.sided":
        ci = [esti2s - z2s * np.sqrt(esti2s * (1 - esti2s) / ni2s), esti2s + z2s * np.sqrt(esti2s * (1 - esti2s) / ni2s)]
    elif alternative == "less":
        ci = [0, esti1s + z1s * np.sqrt(esti1s * (1 - esti1s) / ni1s)]
    elif alternative == "greater":
        ci = [esti1s - z1s * np.sqrt(esti1s * (1 - esti1s) / ni1s), 1]
    else:
        raise ValueError("alternative mis-specified")
    return ci

def binSOC(y, n, conf_level=0.95, alternative="two.sided"):
    esti = y / n
    if alternative == "less":
        kappa = norm.ppf(conf_level)
        eta = (kappa**2) / 3 + 1/6
        gamma1 = ((13/18) * kappa**2 + 17/18) * (-1)
        gamma2 = (kappa**2) / 18 + 7/36
        midpo = (y + eta) / (n + 2 * eta)
        ci = [0, midpo + kappa * np.sqrt(esti * (1 - esti) + (gamma1 * esti * (1 - esti) + gamma2) / n) / np.sqrt(n)]
    elif alternative == "greater":
        kappa = norm.ppf(conf_level)
        eta = (kappa**2) / 3 + 1/6
        gamma1 = ((13/18) * kappa**2 + 17/18) * (-1)
        gamma2 = (kappa**2) / 18 + 7/36
        midpo = (y + eta) / (n + 2 * eta)
        ci = [midpo - kappa * np.sqrt(esti * (1 - esti) + (gamma1 * esti * (1 - esti) + gamma2) / n) / np.sqrt(n), 1]
    elif alternative == "two.sided":
        kappa = norm.ppf(1 - (1 - conf_level) / 2)
        eta = (kappa**2) / 3 + 1/6
        gamma1 = ((13/18) * kappa**2 + 17/18) * (-1)
        gamma2 = (kappa**2) / 18 + 7/36
        midpo = (y + eta) / (n + 2 * eta)
        val = kappa * np.sqrt(esti * (1 - esti) + (gamma1 * esti * (1 - esti) + gamma2) / n) / np.sqrt(n)
        ci = [midpo - val, midpo + val]
    else:
        raise ValueError("alternative mis-specified")
    return [min(ci[0], esti), max(ci[1], esti)]

def binCP(y, n, conf_level=0.95, alternative="two.sided"):
    lower, upper = 0, 1
    if alternative == "two.sided":
        if y != 0:
            lower = beta.ppf((1 - conf_level) / 2, y, n - y + 1)
        if y != n:
            upper = beta.ppf(1 - (1 - conf_level) / 2, y + 1, n - y)
    elif alternative == "less":
        if y != n:
            upper = beta.ppf(conf_level, y + 1, n - y)
        lower = 0
    elif alternative == "greater":
        if y != 0:
            lower = beta.ppf(1 - conf_level, y, n - y + 1)
        upper = 1
    return [lower, upper]

def binWidth(n, p, conf_level=0.95, alternative="two.sided", method="CP"):
    if n < 3:
        raise ValueError("nmax must be at least 3")
    if not (isinstance(n, (int, float)) or (isinstance(n, (list, np.ndarray)) and len(n) == 2)):
        raise ValueError("n must be either a single integer or a vector of two integers")
    if not (0 <= conf_level <= 1):
        raise ValueError("conf.level must be a value between 0 and 1")
    if not (0 <= p <= 1):
        raise ValueError("p.hyp must be a value between 0 and 1")
    
    methods = {"CP": binCP, "Blaker": binCP, "AC": binAC, "Score": binWilson, "Wald": binWald, "SOC": binSOC}
    if method not in methods:
        raise ValueError(f"method must be one of {list(methods.keys())}")
    
    func = methods[method]
    
    def l_ind_bin(y, n, p, conf_level, alternative, method_func):
        int_val = method_func(y, n, conf_level=conf_level, alternative=alternative)
        if alternative == "less":
            return int_val[1] - p
        elif alternative == "greater":
            return p - int_val[0]
        elif alternative == "two.sided":
            return int_val[1] - int_val[0]
        return 0

    def bin_prob(y, n, p):
        from scipy.special import comb
        return comb(n, y) * (p**y) * ((1 - p)**(n - y))

    yvec = np.arange(0, n + 1)
    lvec = []
    probvec = []
    for y in yvec:
        lvec.append(l_ind_bin(y, n, p, conf_level, alternative, func))
        probvec.append(bin_prob(y, n, p))
        
    exp_ci_length = np.sum(np.array(lvec) * np.array(probvec))
    return {"expCIWidth": exp_ci_length, "alternative": alternative, "p": p, "n": n, "_class": "binWidth"}

# r2py:entity:tidy
def tidy(x, **kwargs):
    if isinstance(x, dict) and x.get("_class") == "binWidth":
        df = pd.DataFrame([ {k: v for k, v in x.items() if k != "_class"} ])
        return df.rename(columns={"expCIWidth": "ci.width"})
    else:
        raise NotImplementedError("No tidy method for this object class.")

# r2py:entity:bw
bw = binWidth(100, 0.1)
print(bw)
# r2py:entity:tidy
print(tidy(bw))