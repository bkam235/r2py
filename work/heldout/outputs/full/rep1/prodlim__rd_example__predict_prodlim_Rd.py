# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# r2py:entity:dat
def sim_surv(n):
    """
    Approximates SimSurv logic.
    SimSurv creates two binary variables X1, X2 and uses them in a Cox-Weibull model
    to generate event times and censoring times.
    """
    np.random.seed(42)
    # Simulating X1, X2 as binomials
    x1 = np.random.binomial(1, 0.5, n)
    x2 = np.random.binomial(1, 0.5, n)
    
    # Simulating event times based on a simple additive effect of X1 and X2
    # Based on regression(m, from_val="X1", to="eventtime") <- 1
    # Using a Weibull distribution (scale 1/100 in R usually refers to lambda or 1/alpha)
    def generate_weibull(coefs, X):
        # Base hazard modified by linear predictor
        # lambda * exp(sum(beta*X))
        lambda_base = 0.01
        linear_predictor = np.dot(X, coefs)
        # To simulate survival time: T = (-log(U) / (lambda * exp(LP)))^(1/shape)
        # Assuming shape=1 (exponential) for simplicity as it's the baseline for many SimSurv calls
        return -np.log(np.random.random(len(X))) / (lambda_base * np.exp(linear_predictor))

    X = np.column_stack([x1, x2])
    event_times = generate_weibull(np.array([1, 1]), X)
    cen_times = generate_weibull(np.array([0, 0]), X) # censoring baseline
    
    time = np.minimum(event_times, cen_times)
    status = (event_times <= cen_times).astype(int)
    
    return pd.DataFrame({'time': time, 'status': status, 'X1': x1, 'X2': x2})

# r2py:entity:fit
class ProdlimWrapper:
    """
    Wrapper to emulate prodlim functionality using lifelines.
    """
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.kmf = KaplanMeierFitter()
        
        if formula == "Hist(time,status)~1":
            self.kmf.fit(data['time'], event_observed=data['status'])
            self.covariate_type = 1
            self.strata_vars = []
        else:
            # Handle strata: Hist(time,status)~X1+X2
            # prodlim with covariates often treats them as strata for KM
            self.covariate_type = 2
            # Extract variables from formula (very basic parse)
            self.strata_vars = [v.strip() for v in formula.split('~')[1].split('+')]
            
    def predict(self, times, newdata=None, mode="list", bytime=False):
        if self.covariate_type == 1:
            # Global KM
            surv_probs = self.kmf.survival_function_at_times(times).values.flatten()
            # R's predict returns NA if time is beyond max time
            max_t = self.kmf.survival_function_.index.max()
            surv_probs = np.where(times <= max_t, surv_probs, np.nan)
            
            if mode == "matrix":
                return surv_probs.reshape(1, -1)
            return surv_probs
        else:
            # Strata-based KM
            if newdata is None:
                raise ValueError("newdata is required when there are strata")
            
            # In prodlim, when formula is X1+X2, it creates combinations of strata
            results = []
            strata_combinations = newdata[self.strata_vars].drop_duplicates()
            
            # We need to fit a KM for every unique combination of strata present in original data
            for _, row in strata_combinations.iterrows():
                mask = pd.DataFrame(False, index=self.data.index, columns=self.strata_vars)
                for var in self.strata_vars:
                    mask[var] = self.data[var] == row[var]
                
                final_mask = mask.all(axis=1)
                stratum_data = self.data[final_mask]
                
                kmf_s = KaplanMeierFitter()
                kmf_s.fit(stratum_data['time'], event_observed=stratum_data['status'])
                
                s_probs = kmf_s.survival_function_at_times(times).values.flatten()
                max_t_s = kmf_s.survival_function_.index.max()
                s_probs = np.where(times <= max_t_s, s_probs, np.nan)
                results.append(s_probs)
            
            results = np.array(results) # Shape: (N_strata, N_times)
            
            if mode == "matrix":
                if bytime:
                    return results.T
                return results
            
            # For mode="list", return as dict of arrays
            return {f"stratum_{i}": res for i, res in enumerate(results)}

# Execution
dat = sim_surv(400)
fit = ProdlimWrapper("Hist(time,status)~1", data=dat)

# predict the survival probs at selected times
# r2py:entity:predict
print(fit.predict(times=np.array([3, 5, 10])))

# NA is returned when the time point is beyond the range
# r2py:entity:predict_1
print(fit.predict(times=np.array([-1, 0, 10, 100, 1000, 10000])))

# when there are strata, newdata is required
# r2py:entity:mfit
mfit = ProdlimWrapper("Hist(time,status)~X1+X2", data=dat)
# R's dat[18:21,] is 0-indexed 17:21 (inclusive 17, 18, 19, 20)
# r2py:entity:predict_2
newdata_subset = dat.iloc[17:21]
print(mfit.predict(times=np.array([-1, 0, 10, 100, 1000, 10000]), newdata=newdata_subset))

# this can be requested in matrix form
# r2py:entity:predict_3
print(mfit.predict(times=np.array([-1, 0, 10, 100, 1000, 10000]), newdata=newdata_subset, mode="matrix"))

# and even transposed
# r2py:entity:predict_4
print(mfit.predict(times=np.array([-1, 0, 10, 100, 1000, 10000]), newdata=newdata_subset, mode="matrix", bytime=True))