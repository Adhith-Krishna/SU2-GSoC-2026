# Adhith Krishna - GSoC 2026 Assignment 3
# Hand Calculations: Skin Friction Coefficient Comparison
# Compares SU2 SST results against two analytical methods from:
# Pearce, B. (1970). TOR-0066(5758-02)-3. The Aerospace Corporation.

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ----------------------------------------------------------------------
#  Flow Conditions
# ----------------------------------------------------------------------

fsv = 69.4448 # Free Stream Velocity (m/s)
nu = 1.84592e-5 / 1.32905 # Kinematic Viscosity (m^2/s)

# ----------------------------------------------------------------------
#  Reading SU2 Surface Flow Data 
# ----------------------------------------------------------------------
# AI Disclaimer: The following function required help from Claude in 
# order to correctly parse the VTK file.

def parse_vtk_surface(filepath):
    with open(filepath, 'r') as f:
        lines = f.read().split()

    # Find POINTS section
    idx = lines.index('POINTS')
    n_points = int(lines[idx + 1])
    start = idx + 3
    coords = []
    for i in range(n_points):
        x = float(lines[start + i*3])
        coords.append(x)
    x_arr = np.array(coords)

    # Find Skin_Friction_Coefficient VECTORS section
    idx_cf = lines.index('Skin_Friction_Coefficient')
    start_cf = idx_cf + 2  # skip "double" and newline
    cf_arr = []
    for i in range(n_points):
        cf_x = float(lines[start_cf + i*3])  # x-component only
        cf_arr.append(cf_x)
    cf_arr = np.array(cf_arr)

    return x_arr, cf_arr

x, cf_su2 = parse_vtk_surface('surface_flow.vtk')
# AI assist ends here

# Remove leading edge point in order to avoid singularity
mask = x > 0.005
x     = x[mask]
cf_su2 = cf_su2[mask]

# Sort by x
idx_sort = np.argsort(x)
x        = x[idx_sort]
cf_su2   = cf_su2[idx_sort]

Rex = fsv * x / nu

# ----------------------------------------------------------------------
#  Analytical Formulas
# ----------------------------------------------------------------------

def cf_prandtl(Rex):
    return 0.0592 * Rex**(-0.2)

def cf_schultz_grunow(Rex):
    return 0.37 * (np.log10(Rex + 3000))**(-2.584)

cf_p  = cf_prandtl(Rex)
cf_sg = cf_schultz_grunow(Rex)

# ----------------------------------------------------------------------
#  Plot
# ----------------------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(x, cf_su2, 'k-',  linewidth=2,   label='SU2 SST (RANS)')
plt.plot(x, cf_p,   'b--', linewidth=1.5,  label='Prandtl')
plt.plot(x, cf_sg,  'r-.',  linewidth=1.5, label='Modified Schultz-Grunow')
plt.xlabel('x (m)', fontsize=12)
plt.ylabel('$C_f$', fontsize=12)
plt.title('Skin Friction Coefficient in SU2 SST vs Analytical Methods\nMach 0.2, Re = 5x10⁶, Adiabatic Wall', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/cf_comparison_flatplateturb.png', dpi=150)
plt.show()
print("Plot has been saved.")

# ----------------------------------------------------------------------
#  Comparison Table
# ----------------------------------------------------------------------
x_check = [0.5, 1.0, 1.5, 2.0]
print("\n----------- Skin Friction Comparison (Pearce 1970 methods) -----------")
print(f"{'x (m)':<8} {'Re_x':<12} {'SU2':>8} {'Prandtl':>10} {'Err%':>7} {'S-G':>10} {'Err%':>7}")
print("-" * 70)
for xv in x_check:
    idx = np.argmin(np.abs(x - xv))
    su2 = cf_su2[idx]
    rex = Rex[idx]
    p   = cf_prandtl(rex)
    sg  = cf_schultz_grunow(rex)
    ep  = (su2 - p)  / su2 * 100
    esg = (su2 - sg) / su2 * 100
    print(f"{xv:<8.1f} {rex:<12.3e} {su2:>8.5f} {p:>10.5f} {ep:>7.2f} {sg:>10.5f} {esg:>7.2f}")