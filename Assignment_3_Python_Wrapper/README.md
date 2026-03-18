# Assignment 3 - Python Wrapper Test Case

## Case Description
Turbulent flow over a flat plate at Mach 0.2 and a Reynolds Number of 5x10^6 using the
SU2 Python Wrapper. The case uses the SST turbulence model under a steady state adiabtic 
wall condition.

## Files 
| File                              | Description                       |
|-----------------------------------|-----------------------------------|
| `turb_SST_flatplate.cfg`          | SU2 configuration file            |
| `mesh_flatplate_turb_137x97.su2`  | Structured 137×97 mesh            |
| `run_flatplate.py`                | Python wrapper script             |
| `results/`                        | Output plots and Paraview files   |

## Main Configuration Details
| Parameter                 | Value             | Reason                            |
|---------------------------|-------------------|-----------------------------------|
| Solver                    | RANS              | Turbulent flow                    |
| Turbulence model          | SST               | Adequate boundary layer resolution|
| Mach number               | 0.2               | Low-speed compressible            |
| Reynolds number           | 5×10⁶             | Fully turbulent regime            |
| CFL                       | 3.0               | Higher CFL caused divergence      |
| Convergence target        | rms[ρ] < 10⁻⁹     | To maintain high accuracy         |

## Convergence
The simulation converged after 26,757 iterations to rms[ρ] = -9.00006. CFL = 3.0 was required for stability — higher values caused divergence due to instability of the SST turbulence model at high Reynolds number.

## Debugging and Issues encountered
- Initially focused on obtaining a residual of order of magnitude of -15 as it was the default value in the
CHT configuration. This caused the simulation to not converge regardless of adjustments made in configuration.
Hence the convergence criteria for residual was reduced to be of order of magnitude of -9.
- CFL = 10 caused late-stage divergence around iteration 600 due to SST instability. Reduced to CFL = 3.0 for stable convergence. A CFL of 5 was also experimented with but 3 was chosen due to being more reliable.
- ITER interaction with Python wrapper required understanding of SU2's internal iteration architecture. Run() executes all ITER iterations per call. Sorting this out required a bit of time to ensure that the wrapper and
the solver worked properly.

## Results 

### Hand 
Using the Schlichting turbulent flat plate formula:
