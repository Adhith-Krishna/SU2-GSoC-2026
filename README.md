## Overview
This repository contains my completed pre-selection assignments for GSoC 2026 with Stichting SU2.
The assignments cover mesh generation, simulation setup, Python wrapper usage, source code
modification, and post-processing.

## Assignments

### Assignment 2 - Axisymmetric Turbulent Jet
Set up a turbulent jet simulation from scratch. This involved generating a 2D axisymmetric
mesh using Gmsh, configuring SU2 for incompressible RANS with the SST turbulence model,
running the simulation at Re = 2000, and comparing the centreline velocity decay against
the PIV/LIF measurements of Fukushima et al. (2001).

### Assignment 3 - Python Wrapper Flat Plate
Compiled SU2 with Python support and ran the classic flat plate test case through the
Python wrapper. Demonstrates direct solver control from Python without a config-driven
workflow.

### Assignment 4 - Spatially Varying Wall Temperature
Extended the flat plate case to apply a non-uniform wall temperature profile using the
Python wrapper's `SetMarkerCustomTemperature` interface. Shows how SU2's Python API
can be used to impose custom boundary conditions that aren't available through the
standard config file.

### Assignment 5 - New Volume Output: Local Speed of Sound
Modified SU2's C++ source (`CFlowIncOutput.cpp`) to add the local speed of sound as
both a volume output field (visible in ParaView) and a screen history output.

## Environment
- SU2 v8.4.0 "Harrier"
- Ubuntu 22.04 (WSL2)
- Python 3.10
- Gmsh 4.x
