# Adhith Krishna - GSoC 2026 Submission Assignment 3
# Simulating turbulent flow over a flat plate using SU2 and a Python wrapper at
# Mach 0.2, Re = 5,000,000 under Steady State Adiabatic Conditions.
# Wrapper format was derived from flatPlate_unsteady_CHT.py from SU2's repository.
# Configuration file used is turb_SST_flatplate.cfg

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import sys
from optparse import OptionParser       # use a parser for configuration
import pysu2                                # imports the SU2 wrapped module

# -------------------------------------------------------------------
#  Main
# -------------------------------------------------------------------

def main():

  # Command line options
  parser=OptionParser()
  parser.add_option("-f", "--file", dest="filename", help="Read config from FILE", metavar="FILE")
  parser.add_option("--parallel", action="store_true",
                    help="Specify if we need to initialize MPI", dest="with_MPI", default=False)

  (options, args) = parser.parse_args()
  options.nDim = int(2)
  options.nZone = int(1)

  # Import mpi4py for parallel run
  if options.with_MPI == True:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
  else:
    comm = 0
    rank = 0

  # Initialize the corresponding driver of SU2, this includes solver preprocessing
  try:
      SU2Driver = pysu2.CSinglezoneDriver(options.filename, options.nZone, comm);
  except TypeError as exception:
    print('A TypeError occured in pysu2.CDriver : ',exception)
    if options.with_MPI == True:
      print('ERROR : You are trying to initialize MPI with a serial build of the wrapper. Please, remove the --parallel option that is incompatible with a serial build.')
    else:
      print('ERROR : You are trying to launch a computation without initializing MPI but the wrapper has been built in parallel. Please add the --parallel option in order to initialize MPI for the wrapper.')
    return
  
  # All Conjugate Heat Transfer segments irrelevant to the Steady State case were removed
  # from the original flatPlate_unsteady_CHT.py wrapper. The remaining segments are retained here.

  if rank == 0:
    print("\n------------------------------ Begin Solver -----------------------------\n")
  sys.stdout.flush()
  if options.with_MPI == True:
    comm.Barrier()

  # Time iteration preprocessing
  SU2Driver.Preprocess(0)
  # Run one time iteration (e.g. dual-time)
  SU2Driver.Run()
  # Postprocess the solver and exit cleanly
  SU2Driver.Postprocess()
  # Update the solver for the next time iteration
  SU2Driver.Update()
  # Monitor the solver and output solution to file if required
  stopCalc = SU2Driver.Monitor(0)
  SU2Driver.Output(0)
  # To free memory and exit the solver
  SU2Driver.Finalize()

# -------------------------------------------------------------------
#  Run Main Program
# -------------------------------------------------------------------

# this is only accessed if running from command prompt
if __name__ == '__main__':
    main()