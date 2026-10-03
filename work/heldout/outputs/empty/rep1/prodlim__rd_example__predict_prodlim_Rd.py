import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# r2py:data_shim:begin
# r2py:entity:dat
def SimSurv(N=400):
    """
    Approximate the R SimSurv function.
    The R source uses lava to simulate eventtime and censtime
    with a coxWeibull distribution (scale = 1/100).
    Regression coeffs for X1 and X2 on eventtime are 1.
    """
    np.random.seed(42)
    X1 = np.random.binomial(1, 0.5, N)
    X2 = np.random.binomial(1, 0.5, N)
    
    # In lava coxWeibull, the hazard is h(t) = scale * t^(shape-1) * exp(X*beta)
    # Here scale=1/100, shape=1 (implicit in the R SimSurv context if not specified), beta=1
    # For shape=1, it's exponential. 
    # Event time: T = -ln(U) / (scale * exp(beta*X1 + beta*X2))
    # However, the R SimSurv provided in the source suggests scale=1/100 is the rate.
    # Let's use the common R lava distribution behavior.
    
    def generate_time(rate, n):
        # For an exponential distribution with rate lambda, T = -ln(U)/lambda
        return -np.log(np.random.uniform(0, 1, n)) / rate

    # eventtime depends on X1, X2
    # lambda_event = (1/100) * exp(1*X1 + 1*X2)
    lambda_event = (1/100) * np.exp(X1 + X2)
    eventtime = -np.log(np.random.uniform(0, 1, N)) / lambda_event
    
    # censtime does not depend on X
    # lambda_cens = 1/100
    lambda_cens = 1/100
    censtime = -np.log(np.random.uniform(0, 1, N)) / lambda_cens
    
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    
    return pd.DataFrame({'time': time, 'status': status, 'X1': X1, 'X2': X2, 
                         'eventtime': eventtime, 'censtime': censtime, 'event': status})
# r2py:data_shim:end

# r2py:entity:fit
class ProdlimWrapper:
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        self.kmf = KaplanMeierFitter()
        
        self.rhs = formula.split('~')[1].strip()
        if self.rhs == '1':
            self.covariate_type = 1 # pooled
            self.kmf.fit(data['time'], event_observed=data['status'])
            self.maxtime = self.kmf.timeline.max()
            self.surv_func = self.kmf.survival_function_
        else:
            self.covariate_type = 2 # strata
            self.strata_cols = self.rhs.split('+')
            self.fitted_kmfs = {}
            for name, group in data.groupby(self.strata_cols):
                kmf_s = KaplanMeierFitter()
                kmf_s.fit(group['time'], event_observed=group['status'])
                self.fitted_kmfs[name] = kmf_s

    def predict(self, times, newdata=None, mode="list", bytime=False):
        times = np.array(times)
        
        if self.covariate_type == 1:
            # prodlim returns 1.0 for t=0 and t < 0 (unless below min time)
            # But for KM, surv(0) is always 1.0.
            # R's predict.prodlim: returns NA for times > maxtime
            results = []
            for t in times:
                if t < 0:
                    results.append(1.0)
                elif t > self.maxtime:
                    results.append(np.nan)
                else:
                    # Lifelines predict handles interpolation
                    results.append(self.kmf.predict(t))
            
            surv_probs = np.array(results)
            if mode == "matrix":
                return surv_probs.reshape(1, -1)
            return surv_probs

        else:
            if newdata is None:
                raise ValueError("newdata is required when there are strata")
            
            results_list = []
            strata_labels = []
            
            for idx, row in newdata.iterrows():
                stratum_val = tuple(row[col] for col in self.strata_cols)
                # Format label like R: "X1=0, X2=0"
                label = ", ".join([f"{col}={row[col]}" for col in self.strata_cols])
                strata_labels.append(label)
                
                if stratum_val in self.fitted_kmfs:
                    kmf_s = self.fitted_kmfs[stratum_val]
                    max_t_s = kmf_s.timeline.max()
                    
                    row_probs = []
                    for t in times:
                        if t < 0:
                            row_probs.append(1.0)
                        elif t > max_t_s:
                            row_probs.append(np.nan)
                        else:
                            row_probs.append(kmf_s.predict(t))
                    results_list.append(np.array(row_probs))
                else:
                    results_list.append(np.full(len(times), np.nan))
            
            res_array = np.array(results_list)
            
            if mode == "matrix":
                if bytime:
                    # Rows are times, Cols are strata
                    return res_array.T
                return res_array
            
            # Return a dictionary simulating the named list
            return {strata_labels[i]: results_list[i] for i in range(len(results_list))}

# --- Main Script ---

# r2py:entity:dat
dat = SimSurv(400)

# r2py:entity:fit
fit = ProdlimWrapper("Hist(time,status)~1", dat)

# predict(fit, times=c(3,5,10))
# r2py:entity:predict
print(fit.predict(times=[3, 5, 10]))

# predict(fit, times=c(-1,0,10,100,1000,10000))
# r2py:entity:predict_1
print(fit.predict(times=[-1, 0, 10, 100, 1000, 10000]))

# r2py:entity:mfit
mfit = ProdlimWrapper("Hist(time,status)~X1+X2", dat)

# R's dat[18:21,] is 0-based 17:21
# r2py:entity:predict_2
newdata_slice = dat.iloc[17:21]

# predict(mfit, times=c(-1,0,10,100,1000,10000), newdata=dat[18:21,])
print(mfit.predict(times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_slice))

# predict(mfit, times=c(-1,0,10,100,1000,10000), newdata=dat[18:21,], mode="matrix")
# r2py:entity:predict_3
print(mfit.predict(times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_slice, mode="matrix"))

# predict(mfit, times=c(-1,0,10,100,1000,10000), newdata=dat[18:21,], mode="matrix", bytime=TRUE)
# r2py:entity:predict_4
print(mfit.predict(times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_slice, mode="matrix", bytime=True))