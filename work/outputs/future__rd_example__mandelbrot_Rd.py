import numpy as np
import matplotlib.pyplot as plt
import time
from concurrent.futures import Future, ThreadPoolExecutor
import sys

# r2py:entity:counts
def mandelbrot(C=None, xmid=None, ymid=None, side=None, resolution=400, max_iter=200):
    """
    Compute Mandelbrot set counts. 
    Matches R's mandelbrot behavior where it returns an array of iterations.
    """
    if C is not None:
        # C is a flat list of complex numbers (the tile)
        res_tile = int(np.sqrt(len(C)))
        C_complex = np.array(C).reshape(res_tile, res_tile)
    else:
        # Full region calculation
        x = np.linspace(xmid - side/2, xmid + side/2, resolution)
        y = np.linspace(ymid - side/2, ymid + side/2, resolution)
        X, Y = np.meshgrid(x, y)
        C_complex = X + 1j * Y

    Z = np.zeros_like(C_complex, dtype=complex)
    counts = np.full(C_complex.shape, max_iter, dtype=int)
    mask = np.full(C_complex.shape, True, dtype=bool)

    for i in range(1, max_iter + 1):
        Z[mask] = Z[mask] * Z[mask] + C_complex[mask]
        diverged = np.abs(Z) > 2
        mask_diverged = mask & diverged
        counts[mask_diverged] = i
        mask[diverged] = False
        if not np.any(mask):
            break
    
    class MandelbrotResult:
        def __init__(self, data, Z_final, maxIter, tau):
            self.data = data
            self.params = {'Z': Z_final, 'maxIter': maxIter, 'tau': tau}
        def __repr__(self):
            return f"Mandelbrot result array {self.data.shape}"
        def __getitem__(self, key):
            return self.data[key]
        def __len__(self):
            return self.data.shape[0]

    return MandelbrotResult(counts, Z, max_iter, 2.0)

# r2py:entity:demo
def mandelbrot_tiles(xmid, ymid, side, nrow, resolution):
    """Generate complex coordinate tiles for the Mandelbrot set."""
    res_tile = resolution // nrow
    tiles = []
    x_start = xmid - side/2
    y_start = ymid - side/2
    
    for i in range(nrow):
        for j in range(nrow):
            tx = np.linspace(x_start + j * res_tile * (side/resolution), 
                             x_start + (j+1) * res_tile * (side/resolution), res_tile)
            ty = np.linspace(y_start + i * res_tile * (side/resolution), 
                             y_start + (i+1) * res_tile * (side/resolution), res_tile)
            X, Y = np.meshgrid(tx, ty)
            tiles.append((X + 1j * Y).flatten('F').tolist())
    return tiles

# r2py:entity:str
def str_summary(obj):
    """Python equivalent of R's str() for MandelbrotResult."""
    data = obj.data
    z_attr = obj.params['Z']
    
    flat_data = data.flatten('F')
    preview = " ".join(map(str, flat_data[:10]))
    print(f"'Mandelbrot' int [1:{data.shape[0]}, 1:{data.shape[1]}] {preview} ...")
    print(f" - attr(*, \"params\")=List of 3")
    
    z_flat = z_attr.flatten('F')
    def format_complex(c):
        r = float(c.real)
        i = float(c.imag)
        # R's g formatter for complex numbers:
        # Approximate by using %g and removing trailing zeros/dots
        r_str = f"{r:g}"
        i_str = f"{i:g}"
        if i >= 0:
            return f"{r_str}+{i_str}i"
        else:
            # i_str already contains the minus sign
            return f"{r_str}{i_str}i"

    z_preview = " ".join([format_complex(z) for z in z_flat[:3]])
    print(f"  ..$ Z      : cplx [1:{z_attr.shape[0]}, 1:{z_attr.shape[1]}] {z_preview} ...")
    print(f"  ..$ maxIter: int {obj.params['maxIter']}")
    print(f"  ..$ tau    : num {int(obj.params['tau']) if obj.params['tau'] == int(obj.params['tau']) else obj.params['tau']}")

# --- Start of translation ---

# Basic usage
# r2py:entity:counts
counts = mandelbrot(xmid=-0.75, ymid=0, side=3)
# r2py:entity:str
str_summary(counts)

# r2py:entity:plot
plt.imshow(counts.data)
plt.axis('off')
plt.show()

# r2py:entity:demo
def plot_what_is_done(counts_list):
    global n
    for kk in range(len(counts_list)):
        f = counts_list[kk]
        if not isinstance(f, Future):
            continue
        if not f.done():
            continue

        print(f"Plotting tile #{kk+1} of {n} ...")
        val = f.result()
        counts_list[kk] = val
        
        plt.subplot(int(np.sqrt(n)), int(np.sqrt(n)), kk + 1)
        plt.imshow(val.data)
        plt.axis('off')
    
    plt.draw()
    plt.pause(0.1)
    return counts_list

# r2py:entity:demo
options_mock = {
    "future.demo.mandelbrot.region": 1,
    "future.demo.mandelbrot.nrow": 3,
    "future.demo.mandelbrot.resolution": 400,
    "future.demo.mandelbrot.delay": True
}

region_val = options_mock.get("future.demo.mandelbrot.region", 1)
if not isinstance(region_val, list):
    if region_val == 1:
        region = {"xmid": -0.75, "ymid": 0.0, "side": 3.0}
    elif region_val == 2:
        region = {"xmid": 0.283, "ymid": -0.0095, "side": 0.00026}
    elif region_val == 3:
        region = {"xmid": 0.282989, "ymid": -0.01, "side": 3e-8}
    else:
        region = {"xmid": -0.75, "ymid": 0.0, "side": 3.0}

nrow = options_mock.get("future.demo.mandelbrot.nrow", 3)
resolution = options_mock.get("future.demo.mandelbrot.resolution", 400)
delay_opt = options_mock.get("future.demo.mandelbrot.delay", False)

if delay_opt is True:
    def delay(counts_obj):
        time.sleep(1.0)
elif callable(delay_opt):
    delay = delay_opt
else:
    def delay(counts_obj):
        pass

Cs = mandelbrot_tiles(xmid=region["xmid"], ymid=region["ymid"], 
                     side=region["side"], nrow=nrow, 
                     resolution=resolution)

plt.figure(figsize=(8, 8))
n = len(Cs)
for ii in range(n):
    plt.subplot(int(np.sqrt(n)), int(np.sqrt(n)), ii + 1)
    plt.text(0.5, 0.5, f"Future #{ii+1}\nunresolved", 
             ha='center', va='center', fontsize=12)
    plt.axis('off')
plt.pause(0.1)

print(f"Creating {n} Mandelbrot tiles:", end="")
executor = ThreadPoolExecutor()
counts_demo = []

def future_task(ii, C_tile):
    # Match the sequence: print "Calculating...", then compute, then delay, then " done"
    print(f"Calculating tile #{ii+1} of {n} ...", end="")
    fit = mandelbrot(C=C_tile, resolution=resolution)
    delay(fit)
    print(f" done", end="")
    return fit

for ii in range(n):
    print(f" {ii+1}", end="")
    C = Cs[ii]
    f = executor.submit(future_task, ii, C)
    counts_demo.append(f)

print(".")

while True:
    counts_demo = plot_what_is_done(counts_demo)
    if not any(isinstance(item, Future) for item in counts_demo):
        break

plt.show()
print("SUGGESTION: Try to rerun this demo after changing strategy for how futures are resolved, e.g. plan(multisession).\n")