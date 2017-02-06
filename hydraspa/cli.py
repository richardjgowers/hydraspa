"""Parallel Raspa setup creator

Usage:
  hydraspa split <dirname> [-n <N> -c <C> (-P <P>...)]
  hydraspa check <dirname>
  hydraspa gather <dirname>
  hydraspa --version

Options:
  -h --help
  --version                       Show the version
  -n NTASKS, --ntasks NTASKS      Number of duplicates per pressure point [default: 1]
  -c NCYCLES, --ncycles NCYCLES   Number of cycles to perform *each* sim for
  -P, --pressures                 Define list of pressures in kPa

"""
