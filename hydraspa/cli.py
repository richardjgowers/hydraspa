"""Parallel Raspa setup creator

Quantities such as cycles and pressures can be defined using 'k' and
'M' suffixes, for example '4.2k' will be interpreted as '4200', and
'1M' as 1000000.

 - "create" makes a Raspa GCMC input
 - "split" makes many Raspa inputs from a single template
 - "poreblazer" makes a poreblazer input
 - "grab" fetch a single structure from database


Usage:
  hydraspa list (structures | gases | forcefields)
  hydraspa poreblazer -s <struc>
  hydraspa create (-s <struc> | -l <file>) -g <gas> -f <ff> -o <outdir>
  hydraspa split <dirname> -P <P> -T <T> -c <C> [-n <N>]
  hydraspa check <dirname>
  hydraspa gather <dirname>
  hydraspa grab <struc> [-o <outdir>]
  hydraspa --version

Options:
  -h --help           Help!
  --version           Show the version
  -s STRUCTURE        Name of structure from database to use.  Must match one
                      available in `list structures`
  -l STRUCTURE_FILE   Path to structure file to use.
  -g GAS              Name of gas to use.  Must match one in `list gases`
  -f FORCEFIELD       Name of forcefield.
  -o OUTDIR           Where to place output files for create
  -P PRESSURES        Define comma separated pressures in Pa.  Can use
                      k/M suffixes
                      eg "-P 10k,20.5k,30k"
  -T TEMPERATURES     Comma separated temperatures.
                      eg "-T 208.0,214.0"
  -c NCYCLES          Number of cycles to perform *each* sim for. Can use
                      k/M suffixes, eg "-c 2.5M"
  -n NTASKS           Number of duplicates per pressure point [default: 1]

"""
