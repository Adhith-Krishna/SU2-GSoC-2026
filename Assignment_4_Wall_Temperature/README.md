# Assignment 4 - Python Wrapper with Wall Temperature
**Author:** Adhith Krishna | VIT Vellore | GSoC 2026 — Stichting SU2

## Case Description
Turbulent flow over a flat plate at Mach 0.2 and a Reynolds Number of 5x10^6 using the
SU2 Python Wrapper. The case uses the SST turbulence model with a spatially varying temperature
case. This was built upon the code designed for 

## Files 
| File                              | Description                       |
|-----------------------------------|-----------------------------------|
| `turb_SST_flatplate.cfg`          | SU2 configuration file            |
| `mesh_flatplate_turb_137x97.su2`  | Structured 137×97 mesh            |
| `run_flatplate_wall_temp.py`      | Python wrapper script             |
| `results/`                        | Output plots and Paraview files   |
| `hand_calculations.py`            | Validation of RANS model using py |

## Main Configuration Details
| Parameter                 | Value             | Reason                            |
|---------------------------|-------------------|-----------------------------------|
| Solver                    | RANS              | Turbulent flow                    |
| Turbulence model          | SST               | Adequate boundary layer resolution|
| Mach number               | 0.2               | Low-speed compressible            |
| Reynolds number           | 5×10⁶             | Fully turbulent regime            |
| CFL                       | 5.0               | Higher CFL caused divergence      |
| Convergence target        | rms[ρ] < 10⁻⁹     | To maintain high accuracy         |

## Configuration Changes from Assignment 3

| Parameter | Assignment 3 | Assignment 4 | Reason |
|-----------|-------------|-------------|--------|
| Wall BC | `MARKER_HEATFLUX= (wall, 0.0)` | `MARKER_ISOTHERMAL= (wall, 300.0)` | Enable temperature BC |
| Python control | None | `MARKER_PYTHON_CUSTOM= (wall)` | Allow wrapper to override |
| Multigrid | `MGLEVEL= 3` | `MGLEVEL= 0` | Required — MARKER_PYTHON_CUSTOM conflicts with multigrid data structures in SU2 v8.4 |


## Convergence
The simulation converged after 92,572 iterations to rms[ρ] = -9.00001.
Convergence was slower than Assignment 3 due to `MGLEVEL= 0` removing multigrid 
acceleration. CFL = 3.0 maintained throughout.

## Debugging and Issues encountered
- **Multigrid conflict:** Using `MARKER_PYTHON_CUSTOM` with `MGLEVEL > 0` caused a 
null pointer crash in `CSysMatrix::BuildILUPreconditioner`. Setting `MGLEVEL= 0` 
resolves this. This made the simulation process slower, however the run no longer 
crashed.

## Results 
<img width="539" height="605" alt="Screenshot 2026-03-18 172211" src="https://github.com/user-attachments/assets/75b803ad-a8ce-4a36-ba42-b38348231c7c" />
<img width="469" height="642" alt="Screenshot 2026-03-18 172705" src="https://github.com/user-attachments/assets/a8329e1b-1dfc-431e-be96-39899ad59066" />

## References
Pearce, B. (1970). A Comparison of Four Simple Calculation Methods for the Compressible Turbulent Boundary Layer on a Flat Plate. TOR-0066(5758-02)-3. The Aerospace Corporation.
