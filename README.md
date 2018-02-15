# Hydraspa

[![Build Status](https://travis-ci.org/richardjgowers/hydraspa.svg?branch=master)](https://travis-ci.org/richardjgowers/hydraspa)
[![codecov](https://codecov.io/gh/richardjgowers/hydraspa/branch/master/graph/badge.svg)](https://codecov.io/gh/richardjgowers/hydraspa)

Hydraspa (hydra + Raspa) is a Python package for preparing GCMC gas adsorption simulation inputs for the [Raspa](https://github.com/numat/RASPA2) simulation package.


Permission to use the structures from the [CoRe MOF Database](http://gregchung.github.io/CoRE-MOFs/) has kindly been given by [Dr. Yongchul G. Chung](https://github.com/gregchung) of [Pusan National University](http://gregchung.github.io/).


## Installing hydraspa

```bash
git clone https://github.com/richardjgowers/hydraspa.git

cd hydraspa

pip install -r requirements.txt .

```


## Using hydraspa

hydraspa is designed to be used via the command line to prepare and analyse simulation inputs:


```bash
# Create a simulation template of CO2 in IRMOF-1
hydraspa create -s IRMOF-1 -g CO2 -f UFF -o myCO2sim

# Split the template into many temperatures and pressures
hydraspa split myCO2sim/ -p 10k,20k,30k -T  278.0,298.0 -c 20k

# Gather the results once the simulation has been done
hydraspa gather myCO2sim/

```


## Citing

If this software is useful in your research, please consider citing the following sources:

[D. Nazarian, J. Camp, Y.G. Chung, R.Q. Snurr, D.S. Sholl, "Large-Scale Refinement of Metal Organic Framework Structures Using DFT," Chemistry of Materials, 2016](https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.6b04226)

[Y.G. Chung, J. Camp, M. Haranczyk, B.J. Sikora, W. Bury, V. Krungleviciute, T. Yildirim, O.K. Farha, D.S. Sholl, R.Q. Snurr, "Computation-Ready, Experimental Metal-Organic Frameworks: A Tool to Enable High-Throughput Computation of Nanoporous Crystals," Chemistry of Materials, 2014, 26 (21), pp 6185–6192](https://pubs.acs.org/doi/abs/10.1021/cm502594j)

[A. K. Rappe, C. J. Casewit, K. S. Colwell, W. A. Goddard III, and W. M. Skiff "UFF, a full periodic table force field for molecular mechanics and molecular dynamics simulations" Journal of the American Chemical Society, 1992, 114 (25) pp 10024–10035](https://pubs.acs.org/doi/abs/10.1021/ja00051a040)

## Contributing

Hydraspa is actively being used and developed, if you encounter any issues drop me a line on the issue tracker.
