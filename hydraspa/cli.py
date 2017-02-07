"""Parallel Raspa setup creator

Quantities such as cycles and pressures can be defined using 'k' and 'M' suffixes,
for example '4.2k' will be interpreted as '4200', and '1M' as 1000000.

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
  -P, --pressures                 Define list of pressures in Pa

"""
