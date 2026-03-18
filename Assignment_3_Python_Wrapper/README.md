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
| `hand_calculations.py`            | Validation of RANS model using py |

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

### CFD Model Result
<img width="854" height="446" alt="Screenshot 2026-03-17 210216" src="https://github.com/user-attachments/assets/ea20337b-7e57-4ca8-ad36-12423deb38ba" />
<img width="821" height="370" alt="Screenshot 2026-03-17 210318" src="https://github.com/user-attachments/assets/35c90aa8-5267-4eb3-81f9-dcf897799d28" />
<img width="460" height="635" alt="Screenshot 2026-03-17 211329" src="https://github.com/user-attachments/assets/7492d6c3-438f-4fdf-b289-c75fa9b3f3bf" />

### Numerical Calculation Result
<img width="1000" height="600" alt="cf_comparison_flatplateturb" src="https://github.com/user-attachments/assets/8b399d2e-47fd-47c8-a31e-7c5bb3f711ee" />

### Error Percentage between Numerical and RANS Model
| x (m) | Re_x | SU2 Cf | Prandtl Cf | Prandtl Err% | Schultz-Grunow Cf | S-G Err% |
|-------|------|--------|------------|--------------|-------------------|----------|
| 0.5 | 2.488×10⁶ | 0.00295 | 0.00311 | -5.48 | 0.00306 | -3.67 |
| 1.0 | 5.060×10⁶ | 0.00266 | 0.00270 | -1.50 | 0.00271 | -1.82 |
| 1.5 | 7.422×10⁶ | 0.00252 | 0.00250 | +0.67 | 0.00254 | -0.99 |
| 2.0 | 1.000×10⁷ | 0.00241 | 0.00236 | +2.36 | 0.00242 | -0.40 |

## References
Pearce, B. (1970). A Comparison of Four Simple Calculation Methods for the Compressible Turbulent Boundary Layer on a Flat Plate. TOR-0066(5758-02)-3. The Aerospace Corporation.
