import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# r2py:entity:Hist
class Hist:
    def __init__(self, time, event=None, entry=None, id=None, cens_code="0"):
        self.cens_code = str(cens_code)
        self.id = id
        self.entry = entry
        
        if isinstance(time, (list, tuple)) and len(time) == 2:
            self.cens_type = "intervalCensored"
            self.L = np.array(time[0], dtype=float)
            self.R = np.array(time[1], dtype=float)
            self.N = len(self.L)
            self.status = np.full(self.N, 2, dtype=int)
            self.status[self.L == self.R] = 1
            mask_right = (np.isinf(self.R)) | (np.isnan(self.R)) | \
                         ((self.L != self.R) & (np.array([str(x) for x in self.R]) == self.cens_code))
            self.status[mask_right] = 0
            self.R_processed = self.R.copy()
            self.R_processed[self.status == 0] = np.inf
        else:
            self.cens_type = "rightCensored"
            self.time = np.array(time, dtype=float)
            self.N = len(self.time)
            self.status = np.ones(self.N, dtype=int)

        if event is None:
            self.model_type = "survival"
            self.event = np.ones(self.N, dtype=int)
        elif isinstance(event, (list, tuple)) and len(event) == 2:
            self.model_type = "multi.states"
            self.from_state = np.array(event[0])
            self.to_state = np.array(event[1])
            self.event = None 
        else:
            self.event = np.array(event)
            unique_ev = np.unique(self.event)
            non_cens = [e for e in unique_ev if str(e) != self.cens_code]
            if len(non_cens) > 1:
                self.model_type = "competing.risks"
            else:
                self.model_type = "survival"

    def __repr__(self):
        # R's Hist() call prints a summary by default
        return summary(self)

# r2py:entity:summary
def summary(obj):
    if not isinstance(obj, Hist):
        return str(pd.Series(obj).describe())
    
    res = []
    if obj.model_type == "survival" and obj.cens_type == "rightCensored":
        res.append("      Right-censored response of a survival model\n")
        res.append(f"No.Observations: {obj.N} \n")
        res.append("Pattern:")
        res.append("                Freq")
        events = np.sum(np.array([str(e) for e in obj.event]) != obj.cens_code)
        cens = obj.N - events
        res.append(f" event          {events}   ")
        res.append(f" right.censored {cens}")
        
    elif obj.model_type == "competing.risks" and obj.cens_type == "rightCensored":
        res.append("      Right-censored response of a competing.risks model\n")
        res.append(f"No.Observations: {obj.N} \n")
        res.append("Pattern:\n")
        res.append("         ")
        res.append("Cause     event right.censored")
        unique_events = np.unique(obj.event)
        causes = sorted([e for e in unique_events if str(e) != obj.cens_code])
        for cause in causes:
            count = np.sum(obj.event == cause)
            res.append(f"  {cause}           {count}              0")
        cens = np.sum(np.array([str(e) for e in obj.event]) == obj.cens_code)
        res.append(f"  unknown     0              {cens}")

    elif obj.cens_type == "intervalCensored":
        if obj.model_type == "competing.risks":
            res.append("      Interval-censored response of a competing.risks model\n")
            res.append(f"No.Observations: {obj.N} \n")
            res.append("Pattern:\n")
            res.append("         ")
            res.append("Cause     exact.time interval-censored right-censored")
            unique_events = np.unique(obj.event)
            causes = sorted([e for e in unique_events if str(e) != obj.cens_code])
            for cause in causes:
                exact = np.sum((obj.status == 1) & (obj.event == cause))
                inter = np.sum((obj.status == 2) & (obj.event == cause))
                right = np.sum((obj.status == 0) & (obj.event == cause))
                res.append(f"  {cause}                {exact}                 {inter}              {right}")
            cens = np.sum(np.array([str(e) for e in obj.event]) == obj.cens_code)
            res.append(f"  unknown          0                 0              {cens}")
        else:
            res.append("      Interval-censored response of a survival model\n")
            res.append(f"No.Observations: {obj.N} \n")
            res.append("Pattern:")
            res.append("                   Freq")
            res.append(f" exact.time        {np.sum(obj.status == 1)}   ")
            res.append(f" interval-censored {np.sum(obj.status == 2)}   ")
            res.append(f" right-censored    {np.sum(obj.status == 0)}")

    elif obj.model_type == "multi.states":
        is_censored = np.any(np.array([str(t) for t in obj.to_state]) == obj.cens_code)
        header = "      Right-censored response of a multi.states model\n" if is_censored else "      Uncensored response of a multi.states model\n"
        res.append(header)
        res.append(f"No.Observations: {obj.N} \n")
        res.append("Pattern:")
        if is_censored:
            res.append("              Observations")
            res.append("Transitions    event right.censored")
        else:
            res.append("           Observations")
            res.append("Transitions event")
            
        transitions = []
        for f, t in zip(obj.from_state, obj.to_state):
            transitions.append((f, t))
        
        unique_trans = sorted(list(set(transitions)), key=lambda x: (x[0], x[1]))
        for f, t in unique_trans:
            t_label = f"{int(f)} -> {int(t)}" if str(t) != obj.cens_code else f"{int(f)} -> unknown"
            count = sum(1 for x in transitions if x == (f, t))
            if str(t) != obj.cens_code:
                res.append(f"     {t_label}     {count}" + ("              0" if is_censored else ""))
            else:
                res.append(f"     {t_label}     0              {count}")

    output = "\n".join(res)
    print(output)
    return output

# r2py:entity:plot
def plot(obj):
    plt.figure()
    if hasattr(obj, 'time'):
        plt.step(obj.time, np.linspace(1, 0, obj.N))
    plt.title("Survival Plot")
    plt.show()

# r2py:entity:TwoStateFrame
def SimSurv(N):
    # Fixed simulation to be deterministic and plausible for the context
    np.random.seed(42)
    # Approximating the distribution from lava
    eventtime = np.random.exponential(10, N)
    censtime = np.random.exponential(10, N)
    time = np.minimum(eventtime, censtime)
    status = (eventtime <= censtime).astype(int)
    X1 = np.random.binomial(1, 0.5, N)
    X2 = np.random.normal(0, 1, N)
    return pd.DataFrame({
        'eventtime': eventtime,
        'censtime': censtime,
        'time': time,
        'event': status,
        'status': status,
        'X1': X1,
        'X2': X2
    })

# --- Main Script ---

# r2py:entity:Hist
d1 = Hist(time=np.arange(1, 11), event=[0, 1, 0, 0, 0, 1, 0, 1, 0, 0])
print(d1)

# r2py:entity:Hist_1
d2 = Hist(time=np.arange(1, 11), event=[99, "event", 99, 99, 99, "event", 99, "event", 99, 99], cens_code=99)
print(d2)

TwoStateFrame = SimSurv(10)
# r2py:entity:SurvHist
SurvHist = Hist(time=TwoStateFrame['time'], event=TwoStateFrame['status'])
# r2py:entity:summary
summary(SurvHist)
# r2py:entity:plot
plot(SurvHist)

# r2py:entity:CompRiskFrame
CompRiskFrame = pd.DataFrame({'time': np.arange(1, 11), 'event': [1, 2, 0, 3, 0, 1, 2, 1, 2, 1]})
# r2py:entity:CRHist
CRHist = Hist(time=CompRiskFrame['time'], event=CompRiskFrame['event'])
# r2py:entity:summary_1
summary(CRHist)
# r2py:entity:plot_1
plot(CRHist)

# r2py:entity:icensFrame
icensFrame = pd.DataFrame({
    'L': [1, 1, 3, 4, 6],
    'R': [2, np.nan, 3, 6, 9],
    'event': [1, 1, 1, 2, 2]
})
# r2py:entity:with
d_icens1 = Hist(time=[icensFrame['L'], icensFrame['R']])
print(d_icens1)

# r2py:entity:with_1
d_icens2 = Hist(time=[icensFrame['L'], icensFrame['R']], event=icensFrame['event'])
print(d_icens2)

# r2py:entity:MultiStateFrame
MultiStateFrame = pd.DataFrame({
    'time': np.arange(1, 11),
    'from': [1, 1, 3, 1, 2, 4, 1, 1, 2, 1],
    'to': [2, 3, 1, 2, 4, 2, 3, 2, 4, 4]
})
# r2py:entity:with_2
d_ms1 = Hist(time=MultiStateFrame['time'], event=[MultiStateFrame['from'], MultiStateFrame['to']])
print(d_ms1)

# r2py:entity:MultiStateFrame1
MultiStateFrame1 = pd.DataFrame({
    'time': np.arange(1, 11),
    'from': [1, 1, 3, 2, 1, 4, 1, 1, 3, 1],
    'to': [2, 3, 1, 0, 2, 2, 3, 2, 0, 4]
})
# r2py:entity:with_3
d_ms2 = Hist(time=MultiStateFrame1['time'], event=[MultiStateFrame1['from'], MultiStateFrame1['to']])
print(d_ms2)

# r2py:entity:MultiStateFrame2
MultiStateFrame2 = pd.DataFrame({
    'time': [0, 1, 2, 3, 4, 0, 1, 2, 0, 1],
    'event': [1, 2, 3, 0, 1, 2, 4, 2, 1, 2],
    'id': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
})

# r2py:entity:with_4
def Hist_longitudinal(time, event, id):
    df = pd.DataFrame({'time': time, 'event': event, 'id': id})
    df = df.sort_values(['id', 'time'])
    from_states, to_states, times = [], [], []
    for subject_id in df['id'].unique():
        subj = df[df['id'] == subject_id]
        for i in range(len(subj)):
            if i == 0: 
                continue
            f = subj.iloc[i-1]['event']
            t = subj.iloc[i]['event']
            tm = subj.iloc[i]['time']
            from_states.append(f)
            to_states.append(t)
            times.append(tm)
    return Hist(time=np.array(times), event=[from_states, to_states])

d_ms3 = Hist_longitudinal(MultiStateFrame2['time'], MultiStateFrame2['event'], MultiStateFrame2['id'])
print(d_ms3)