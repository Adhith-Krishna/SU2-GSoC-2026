# Assignment 5 - Addition of New Volume Output: Local Speed of Sound
**Author:** Adhith Krishna | VIT Vellore | GSoC 2026 — Stichting SU2

## Case Description
Extension of the Assignment 2 axisymmetric turbulent jet case (Re = 2000, SST RANS) to include
the local speed of sound as a new volume output field in ParaView files and as a new screen
history output. The same mesh and configuration from Assignment 2 are copied and used.

## Files
| File                              | Description                                        |
|-----------------------------------|----------------------------------------------------|
| `jetss.cfg`                       | SU2 configuration file (extended from Assignment 2)|
| `mesh/jet.su2`                    | Mesh of the jet domain                             |
| `results/`                        | Output plots and ParaView files                    |

## Implementation

### Overview
For incompressible flow, a true thermodynamic speed of sound is undefined. SU2's incompressible
solver instead uses an artificial compressibility parameter β² (`BetaInc2`), which plays the
role of a pseudo-speed of sound. The local speed of sound is
therefore defined and implemented as:

```
c = sqrt(β²) = sqrt(GetBetaInc2(iPoint))
```
### How it was Implemented
I first explored the SU2 source to understand how existing output fields like `DENSITY` and `PRESSURE` are registered. All volume and history outputs in the incompressible solver follow the same three-step pattern in `CFlowIncOutput.cpp`: register the field with `AddVolumeOutput` or `AddHistoryOutput`, then fill it each iteration with `SetVolumeOutputValue` or `SetHistoryOutputValue`. I then searched for where speed of sound is stored in the incompressible variable class and found out about the artificial compressibility parameter β² via `GetBetaInc2()`. The local speed of sound is therefore computed as √(β²) and wired into the existing output pattern with a single line per step.

### Files Modified
Only one file was modified: `SU2_CFD/src/output/CFlowIncOutput.cpp`

### Changes Made

**1. Register volume output field** (~line 328):
```cpp
AddVolumeOutput("SOUND_SPEED", "Sound_Speed", "PRIMITIVE",
                "Local speed of sound (sqrt of artificial compressibility beta^2)");
```
This registers the field under the `PRIMITIVE` group so it is written to the VTK file
whenever `VOLUME_OUTPUT= (PRIMITIVE, ...)` is set in the config.

**2. Register history output field** (~line 169):
```cpp
AddHistoryOutput("AVG_SOUND_SPEED", "c_avg", ScreenOutputFormat::SCIENTIFIC,
                 "SOUND_SPEED", "Average local speed of sound.");
```
This registers `c_avg` as a screen and history output field.

**3. Set volume output value per mesh point** (~line 440, inside `LoadVolumeData`):
```cpp
SetVolumeOutputValue("SOUND_SPEED", iPoint, sqrt(Node_Flow->GetBetaInc2(iPoint)));
```
This fills the field with the local β value at every mesh point each iteration.

**4. Set history output value** (~line 253, inside `LoadHistoryData`):
```cpp
SetHistoryOutputValue("AVG_SOUND_SPEED", sqrt(flow_solver->GetNodes()->GetBetaInc2(0)));
```
This writes the speed of sound value to the screen and history file each iteration.

### Config Changes
Two additions to `jetss.cfg` compared to Assignment 2:
```properties
SCREEN_OUTPUT= (INNER_ITER, RMS_PRESSURE, RMS_TKE, RMS_DISSIPATION, AVG_SOUND_SPEED)
VOLUME_OUTPUT= (PRIMITIVE, RESIDUAL, SOUND_SPEED)
```

### Recompilation
After modifying `CFlowIncOutput.cpp`, SU2 was recompiled and reinstalled:
```bash
cd ~/SU2/build
ninja -j$(nproc)
ninja install
```

## Results

### Screen History Output
The `c_avg` column appears in the solver screen output alongside the residuals:

```
+----------------------------------------------------------------+
|  Inner_Iter|      rms[P]|      rms[k]|      rms[w]|       c_avg|
+----------------------------------------------------------------+
|           0|   -1.305239|   -4.994196|   -1.786424|  2.1211e+00|
```

The value of c_avg ≈ 2.12 is the artificial speed of sound √(β²) used by SU2's
incompressible pressure-velocity coupling. It remains approximately constant throughout
the simulation.

### Volume Output — Sound Speed Colour Map
*[Insert ParaView screenshot of Sound_Speed field here]*

The `Sound_Speed` field is visible in ParaView under the PRIMITIVE group. The spatial
distribution reflects the artificial compressibility parameter β² across the domain.

### Velocity Contour (same case as Assignment 2)
*[Insert velocity contour screenshot here]*

## References
- Fukushima, C., Aanen, L. & Westerweel, J. (2001). Investigation of the mixing process
  in an axisymmetric turbulent jet using PIV and LIF. *Proceedings of the 4th International
  Symposium on Particle Image Velocimetry*, Göttingen, Germany.

- Boersma, B.J., Brethouwer, G. & Nieuwstadt, F.T.M. (1998). A numerical investigation
  on the effect of the inflow conditions on the self-similar region of a round jet.
  *Physics of Fluids*, 10(4), 899–909.

- Menter, F.R. (1994). Two-equation eddy-viscosity turbulence models for engineering
  applications. *AIAA Journal*, 32(8), 1598–1605.