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
- Minimum and maixmum orthogonality of 73.4324 and 89.9918
- 5 boundary markers named 'jet_inlet', 'nozzle_plate', 'top_wall', 'outlet', 'axis'

## Convergence
All three residuals dropped steadily to approximately rms[P] ≈ -8.3, rms[k] ≈ -8.9, 
rms[ω] ≈ -7.3 before entering a cycle. This indicated the solution is physically 
converged even though the residuals could not be reduced further.

## Debugging and Issues encountered
- `INC_VELOCITY_INIT` was initialised at 0.001 m/s instead of 1.0 m/s by accident, causing a non-physical velocity field. Corrected to match inlet velocity.
- Initially the condition MUSCL was set to YES, which upon taking Dr. Nijso's advice was changed to NO. This stopped
the cycling of the solution residuals at -3 and -4 and helped the solution converge at -8.

## Results 


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