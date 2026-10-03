import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# r2py:entity:dat
def SimSurv(N):
    """
    Simulates survival data mimicking R's SimSurv/lava logic.
    - X1, X2 ~ Binomial(1, 0.5)
    - eventtime ~ Cox-Weibull(scale=0.01, beta=1 for X1, X2)
    - censtime ~ Cox-Weibull(scale=0.01)
    - time = min(eventtime, censtime)
    - status = (eventtime <= censtime)
    """
    np.random.seed(42)
    X1 = np.random.binomial(1, 0.5, N)
    X2 = np.random.binomial(1, 0.5, N)
    
    # In R lava coxWeibull.lvm, the distribution is based on the hazard.
    # For Cox-Weibull with shape=1 (exponential), Time = -log(U) / (scale * exp(beta*X))
    scale = 0.01
    
    # eventtime: hazard = scale * exp(X1 + X2)
    u_event = np.random.random(N)
    eventtime = -np.log(u_event) / (scale * np.exp(X1 + X2))
    
    # censtime: hazard = scale
    u_cens = np.random.random(N)
    censtime = -np.log(u_cens) / scale
    
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    
    return pd.DataFrame({
        'time': time, 
        'status': status, 
        'X1': X1, 
        'X2': X2,
        'eventtime': eventtime,
        'censtime': censtime,
        'event': status
    })

# r2py:entity:fit
class ProdlimWrapper:
    def __init__(self, formula, data):
        self.formula = formula
        self.data = data
        rhs = formula.split("~")[1].strip()
        self.is_stratified = rhs != "1"
        self.models = {}
        
        if not self.is_stratified:
            kmf = KaplanMeierFitter()
            kmf.fit(data['time'], event_observed=data['status'])
            self.models[None] = kmf
        else:
            self.strata_cols = [c.strip() for c in rhs.split("+")]
            for name, group in data.groupby(self.strata_cols):
                kmf = KaplanMeierFitter()
                kmf.fit(group['time'], event_observed=group['status'])
                self.models[name] = kmf

    def predict(self, times, newdata=None, mode="list", bytime=False):
        times = np.array(times)
        
        if not self.is_stratified:
            kmf = self.models[None]
            # R's prodlim: 
            # t <= 0: 1.0
            # 0 < t <= max_t: KM estimate
            # t > max_t: NA
            surv_probs = kmf.survival_function_at_times(times).values
            max_t = kmf.survival_function_.index.max()
            
            res = []
            for t in times:
                if t <= 0:
                    res.append(1.0)
                elif t > max_t:
                    res.append(np.nan)
                else:
                    # lifelines is right-continuous, so this matches KM
                    res.append(kmf.survival_function_at_times(t).values[0])
            
            surv_probs = np.array(res)
            
            if mode == "matrix":
                return surv_probs.reshape(1, -1)
            return surv_probs

        else:
            if newdata is None:
                raise ValueError("newdata is required for stratified models")
            
            results = []
            row_labels = []
            
            for idx, row in newdata.iterrows():
                stratum_key = tuple(row[col] for col in self.strata_cols)
                
                # Label format "X1=1, X2=0"
                label = ", ".join([f"{col}={row[col]}" for col in self.strata_cols])
                row_labels.append(label)
                
                if stratum_key in self.models:
                    kmf_group = self.models[stratum_key]
                    max_t = kmf_group.survival_function_.index.max()
                    
                    probs = []
                    for t in times:
                        if t <= 0:
                            probs.append(1.0)
                        elif t > max_t:
                            probs.append(np.nan)
                        else:
                            probs.append(kmf_group.survival_function_at_times(t).values[0])
                    results.append(np.array(probs))
                else:
                    results.append(np.full(len(times), np.nan))
            
            if mode == "matrix":
                res_array = np.array(results)
                if bytime:
                    return res_array.T
                return res_array
            
            return dict(zip(row_labels, results))

def prodlim(formula, data):
    return ProdlimWrapper(formula, data)

# r2py:entity:predict
def predict(object_fit, times, newdata=None, mode="list", bytime=False):
    return object_fit.predict(times=times, newdata=newdata, mode=mode, bytime=bytime)

# Execution
# r2py:entity:dat
dat = SimSurv(400)
# r2py:entity:fit
fit = prodlim("Hist(time,status)~1", data=dat)
# r2py:entity:predict
print(predict(fit, times=[3, 5, 10]))
# r2py:entity:predict_1
print(predict(fit, times=[-1, 0, 10, 100, 1000, 10000]))
# r2py:entity:mfit
mfit = prodlim("Hist(time,status)~X1+X2", data=dat)
# r2py:entity:predict_2
newdata_subset = dat.iloc[17:21]
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset))
# r2py:entity:predict_3
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix"))
# r2py:entity:predict_4
print(predict(mfit, times=[-1, 0, 10, 100, 1000, 10000], newdata=newdata_subset, mode="matrix", bytime=True))