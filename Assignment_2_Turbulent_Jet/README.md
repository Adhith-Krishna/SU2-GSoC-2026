# Assignment 2 - Axisymmetric, Steady State, Turbulent Test Case
**Author:** Adhith Krishna | VIT Vellore | GSoC 2026 — Stichting SU2

## Case Description
Steady RANS simulation of an axisymmetric turbulent free jet at Re = 2000 using SU2 v8.4.0,
validated against the PIV/LIF measurements of Fukushima et al. (2001) and the DNS of 
Boersma et al. (1998).

## Files 
| File                              | Description                       |
|-----------------------------------|-----------------------------------|
| `jet.cfg`          | SU2 configuration file            |
| `jet.su2`  | Mesh of the jet in SU2 config            |
| `convergence.py`                | Python script to compute graphically plot convergence |
| `results/`                        | Output plots and Paraview files   |

## Main Configuration Details
| Parameter                 | Value             | Reason                            |
|---------------------------|-------------------|-----------------------------------|
| Solver                    | INC_RANS          | Incompressible turbulent flow                    |
| Turbulence model          | SST               | Adequate boundary layer resolution|
| Reynolds number           | 2000              | Matches Boersma and Fukushima et al            |
| CFL                       | 10.0              | CFL of 10 with adaptive CFL on and a maximum of 50     |
| Convergence target        | All RMS values to hit -8     | To maintain high accuracy         |

## Mesh Parameters
- 28,713 nodes and 56,787 elements
- Axisymmetric 2D domain
- Minimum and maximum orthogonality of 73.4324 and 89.9918
- 5 boundary markers named 'jet_inlet', 'nozzle_plate', 'top_wall', 'outlet', 'axis'

## Debugging and Issues encountered
- `INC_VELOCITY_INIT` was initialised at 0.001 m/s instead of 1.0 m/s by accident, causing a non-physical velocity field. Corrected to match inlet velocity.
- Initially the condition MUSCL was set to YES, which upon taking Dr. Nijso's advice was changed to NO. This stopped
the cycling of the solution residuals at -3 and -4 and helped the solution converge at -8.
- Initially the solver was set to 'INC_NAVIER_STOKES' which meant a laminar solve instead of 'INC_RANS'. I wasn't clear with this and therefore the laminar NS
  solve gave incorrect values. My initial assumption was that 'INC_NAVIER_STOKES' method would run a full Direct Navier Stokes simulation and was done to experiment and
  learn how SU2's (assumed) DNS solver would work although it would have been computational extremely expensive.
  
## Results 

### Velocity Contour
<img width="851" height="634" alt="image" src="https://github.com/user-attachments/assets/efb4baab-5c38-4901-9c8d-e085aac51315" />
The jet issues from the nozzle at the origin (bottom-left) and spreads radially as it propagates downstream along the x-axis. This is consistent
with the experimental setup of Fukushima et al. (2001). The colorbar range of 0–1.0 m/s corresponds to the normalised jet exit velocity of 1.0 m/s.

### Centerline velocity decay
<img width="848" height="632" alt="image" src="https://github.com/user-attachments/assets/1a27815a-1523-4573-af79-9ac19af527c2" />
<img width="446" height="319" alt="image" src="https://github.com/user-attachments/assets/3734f707-d3a6-4cfa-9f10-068e1003aacf" />
The decay character is consistent with Fukushima et al, although we use normalized units whereas Fukushima has plotted it using 
dimensional units. Our graph and mesh only simulates up to x=90. This is because the length of the computational domain is taken
equal to 45 orifice diameters as per Boersma et al.

### Convergence Graphs over the last 500 iterations
<img width="790" height="235" alt="image" src="https://github.com/user-attachments/assets/e41cff12-3e7c-4b13-851e-c2ae3ceca698" />
All three residuals dropped steadily from iteration 0 to approximately iteration 2100,
reaching rms[P] ≈ -8.3, rms[k] ≈ -8.9, and rms[ω] ≈ -7.3. Beyond this point the
residuals entered a limit cycle, oscillating within a narrow band of approximately
±0.35 without further reduction. The solution is considered
physically converged at this point.


## References
- Fukushima, C., Aanen, L. & Westerweel, J. (2001). Investigation of the mixing process
  in an axisymmetric turbulent jet using PIV and LIF. *Proceedings of the 4th International
  Symposium on Particle Image Velocimetry*, Göttingen, Germany.

- Boersma, B.J., Brethouwer, G. & Nieuwstadt, F.T.M. (1998). A numerical investigation
  on the effect of the inflow conditions on the self-similar region of a round jet.
  *Physics of Fluids*, 10(4), 899–909.

- Hussein, H.J., Capp, S.P. & George, W.K. (1994). Velocity measurements in a
  high-Reynolds-number, momentum-conserving, axisymmetric, turbulent jet.
  *Journal of Fluid Mechanics*, 258, 31–75.
