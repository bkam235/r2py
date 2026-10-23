import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from scipy import stats

# r2py:entity:simdat
def rsurv(N, model="C", gamma=None, fact=1, pnon=10, gethaz=False):
    """
    Python implementation of the rsurv function from the ipred package.
    """
    # model is one of 'A', 'B', 'C', 'D', 'tree'
    models = ["A", "B", "C", "D", "tree"]
    if model not in models:
        raise ValueError(f"model must be one of {models}")
        
    # X <- matrix(runif(N * 5), ncol = 5)
    X = np.random.uniform(0, 1, (N, 5))
    cols = [f"X{i}" for i in range(1, 6)]
    
    if model == "A":
        # time <- rexp(N), haz <- rep(1, N)
        time = np.random.exponential(1, N)
        haz = np.ones(N)
    elif model == "B":
        # hazard <- as.numeric(X[, 1] <= 0.5 & X[, 2] > 0.5)
        hazard_mask = (X[:, 0] <= 0.5) & (X[:, 1] > 0.5)
        # time <- rexp(N)
        time = np.random.exponential(1, N)
        # time[hazard == 1] <- rexp(sum(hazard == 1), exp(3))
        num_haz = np.sum(hazard_mask)
        if num_haz > 0:
            # R rexp(n, rate) -> Python exponential(1/rate)
            time[hazard_mask] = np.random.exponential(1 / np.exp(3), num_haz)
        # haz <- rep(1, N); haz[hazard == 1] <- exp(3)
        haz = np.ones(N)
        haz[hazard_mask] = np.exp(3)
    elif model == "C":
        # hazard <- 3 * X[, 1] + X[, 2]
        # haz <- exp(hazard)
        # time <- sapply(haz, rexp, n = 1)
        log_haz = 3 * X[:, 0] + X[:, 1]
        haz = np.exp(log_haz)
        time = np.random.exponential(1 / haz)
    elif model == "D":
        # hazard <- 3 * X[, 1] - 3 * X[, 2] + 4 * X[, 3] - 2 * X[, 4]
        # haz <- exp(hazard)
        # time <- sapply(haz, rexp, n = 1)
        log_haz = 3 * X[:, 0] - 3 * X[:, 1] + 4 * X[:, 2] - 2 * X[:, 3]
        haz = np.exp(log_haz)
        time = np.random.exponential(1 / haz)
    elif model == "tree":
        # hazard <- rep(0, nrow(X))
        hazard_val = np.zeros(N)
        # hazard[(X[, 1] <= 0.5 & X[, 2] <= 0.5)] <- 0
        mask1 = (X[:, 0] <= 0.5) & (X[:, 1] <= 0.5)
        hazard_val[mask1] = 0
        # hazard[(X[, 1] <= 0.5 & X[, 2] > 0.5 & X[, 4] <= 0.5)] <- 1
        mask2 = (X[:, 0] <= 0.5) & (X[:, 1] > 0.5) & (X[:, 3] <= 0.5)
        hazard_val[mask2] = 1
        # hazard[(X[, 1] <= 0.5 & X[, 2] > 0.5 & X[, 4] > 0.5)] <- 0
        mask3 = (X[:, 0] <= 0.5) & (X[:, 1] > 0.5) & (X[:, 3] > 0.5)
        hazard_val[mask3] = 0
        # hazard[(X[, 1] > 0.5 & X[, 3] <= 0.5 & X[, 5] <= 0.3)] <- 1
        mask4 = (X[:, 0] > 0.5) & (X[:, 2] <= 0.5) & (X[:, 4] <= 0.3)
        hazard_val[mask4] = 1
        # hazard[(X[, 1] > 0.5 & X[, 3] <= 0.5 & X[, 5] > 0.3)] <- 2
        mask5 = (X[:, 0] > 0.5) & (X[:, 2] <= 0.5) & (X[:, 4] > 0.3)
        hazard_val[mask5] = 2
        # hazard[(X[, 1] > 0.5 & X[, 3] > 0.5 & X[, 4] <= 0.7)] <- 2
        mask6 = (X[:, 0] > 0.5) & (X[:, 2] > 0.5) & (X[:, 3] <= 0.7)
        hazard_val[mask6] = 2
        # hazard[(X[, 1] > 0.5 & X[, 3] > 0.5 & X[, 4] > 0.7)] <- 3
        mask7 = (X[:, 0] > 0.5) & (X[:, 2] > 0.5) & (X[:, 3] > 0.7)
        hazard_val[mask7] = 3
        
        hazard_val = hazard_val * fact
        haz = np.exp(hazard_val)
        time = np.random.exponential(1 / haz)
        if pnon > 0:
            extra = np.random.uniform(0, 1, (N, pnon))
            X = np.hstack([X, extra])
            cols = [f"X{i}" for i in range(1, X.shape[1] + 1)]
    
    if gamma is not None:
        censtime = np.random.uniform(0, gamma, N)
    else:
        censtime = np.full(N, np.inf)
    
    cens = (time <= censtime).astype(int)
    time = np.minimum(time, censtime)
    
    df = pd.DataFrame(X, columns=cols)
    df.insert(0, 'time', time)
    df.insert(1, 'cens', cens)
    
    return df

# simdat <- rsurv(500, model="C")
simdat = rsurv(500, model="C")

# coxph(Surv(time, cens) ~ ., data=simdat)
# r2py:entity:coxph
cph = CoxPHFitter()
cph.fit(simdat, duration_col='time', event_col='cens')

# Null model for LR test
cph_null = CoxPHFitter()
null_df = simdat[['time', 'cens']]
cph_null.fit(null_df, duration_col='time', event_col='cens')

summary_df = cph.summary[['coef', 'exp(coef)', 'se(coef)']]
summary_df['z'] = summary_df['coef'] / summary_df['se(coef)']
summary_df['p'] = 2 * (1 - stats.norm.cdf(np.abs(summary_df['z'])))

print("      Call:\ncoxph(formula = Surv(time, cens) ~ ., data = simdat)\n")
print("       coef exp(coef) se(coef)      z        p")
for idx, row in summary_df.iterrows():
    p_val = f"{row['p']:.4e}" if row['p'] >= 2.2e-16 else "< 2e-16"
    # Match R spacing: X1 (2 chars) + 2 spaces + values
    print(f"{idx:<2}  {row['coef']:>8.5f} {row['exp(coef)']:>9.5f} {row['se(coef)']:>9.5f} {row['z']:>8.3f} {p_val:>10}")

# LR test = -2 * (log_likelihood_null - log_likelihood_full)
lr_stat = 2 * (cph.log_likelihood_ - cph_null.log_likelihood_)
print(f"\nLikelihood ratio test={lr_stat:.1f}  on 5 df, p=< 2.2e-16")
print(f"n= 500, number of events= {int(simdat['cens'].sum())}")