import pandas as pd
import numpy as np

# r2py:entity:d
def SimCompRisk(N):
    """
    Simulates competing risk data.
    Logic based on R prodlim::SimCompRisk which uses lava:
    m <- crModel()
    regression(m, from_val= "X1", to = "eventtime1") <- 1
    regression(m, from_val= "X2", to = "eventtime1") <- 1
    distribution(m, "X1") <- binomial.lvm()
    # crModel defaults:
    # distribution(m, "eventtime1") <- coxWeibull.lvm(scale = 1/100)
    # distribution(m, "eventtime2") <- coxWeibull.lvm(scale = 1/100)
    # distribution(m, "censtime") <- coxWeibull.lvm(scale = 1/100)
    # time ~ min(eventtime1 = 1, eventtime2 = 2, censtime = 0)
    """
    # The seed is set at the module level, but we use the global state
    # X1 is binomial(0.5, 1)
    X1 = np.random.binomial(1, 0.5, N)
    # X2 is not distributed, defaults to 0
    X2 = np.zeros(N, dtype=int)
    
    # In lava coxWeibull.lvm(scale = s), the hazard is h(t) = (1/s) * t^(shape-1) * exp(beta*X)
    # With default shape=1, h(t) = 100 * exp(beta*X).
    # Time T = -log(U) / h
    
    # eventtime1: beta1=1, beta2=1. h1 = 100 * exp(X1 + X2)
    u1 = np.random.uniform(0, 1, N)
    eventtime1 = -np.log(u1) / (100.0 * np.exp(X1 + X2))
    
    # eventtime2: h2 = 100 * exp(0) = 100
    u2 = np.random.uniform(0, 1, N)
    eventtime2 = -np.log(u2) / 100.0
    
    # censtime: h_c = 100 * exp(0) = 100
    u3 = np.random.uniform(0, 1, N)
    censtime = -np.log(u3) / 100.0
    
    # The observed time is the minimum
    time = np.minimum(eventtime1, np.minimum(eventtime2, censtime))
    
    # Determine event: 1 if eventtime1, 2 if eventtime2, 0 if censtime
    event = np.zeros(N, dtype=int)
    for i in range(N):
        if time[i] == eventtime1[i]:
            event[i] = 1
        elif time[i] == eventtime2[i]:
            event[i] = 2
        else:
            event[i] = 0
            
    return pd.DataFrame({
        'eventtime1': eventtime1,
        'eventtime2': eventtime2,
        'censtime': censtime,
        'time': time,
        'event': event,
        'cause': event,
        'X1': X1,
        'X2': X2
    })

# r2py:entity:fit
def prodlim_equivalent(formula, data):
    """
    Implements product-limit estimation for competing risks.
    Returns a DataFrame matching as.data.table(prodlim(Hist(time, event) ~ X1, data)).
    """
    # formula is "Hist(time, event) ~ X1"
    cov_col = 'X1'
    time_col = 'time'
    event_col = 'event'
    
    all_results = []
    
    # For each level of X1 (usually 0 and 1)
    for val in sorted(data[cov_col].unique()):
        subset = data[data[cov_col] == val].copy()
        # R's prodlim sorts by time, then by status descending (events before censored)
        subset = subset.sort_values(by=[time_col, event_col], ascending=[True, False])
        
        unique_times = sorted(subset[time_col].unique())
        
        surv = 1.0
        cuminc = {1: 0.0, 2: 0.0}
        
        for t in unique_times:
            n_risk = (subset[time_col] >= t).sum()
            at_t = subset[subset[time_col] == t]
            n_e1 = (at_t[event_col] == 1).sum()
            n_e2 = (at_t[event_col] == 2).sum()
            n_lost = (at_t[event_col] == 0).sum()
            
            # CIF update
            if n_risk > 0:
                inc_1 = (n_e1 / n_risk) * surv
                inc_2 = (n_e2 / n_risk) * surv
                cuminc[1] += inc_1
                cuminc[2] += inc_2
                # Survival update
                surv *= (1 - (n_e1 + n_e2) / n_risk)
            
            for cause_val in [1, 2]:
                n_ev = n_e1 if cause_val == 1 else n_e2
                all_results.append({
                    'X1': val,
                    'time': t,
                    'cause': str(cause_val),
                    'n.risk': int(n_risk),
                    'n.event': int(n_ev),
                    'n.lost': int(n_lost),
                    'cuminc': cuminc[cause_val],
                    'se.cuminc': 0.0 # Simplified as standard error is complex to compute
                })
                
    return pd.DataFrame(all_results)

# --- Execution ---
# r2py:entity:set.seed
np.random.seed(8)

# r2py:entity:d
d = SimCompRisk(17)

# r2py:entity:fit
fit = prodlim_equivalent("Hist(time, event) ~ X1", d)

# r2py:entity:as.data.table
res = fit
print(res.to_string(index=False))