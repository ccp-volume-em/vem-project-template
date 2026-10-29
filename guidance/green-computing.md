# Green computing

From the guide: [Green computing](https://ccp-volume-em.github.io/guide/green/).

Use computing resources efficiently, and be accountable for the environmental
impact of heavy compute.

- Measure the carbon footprint of heavy jobs. The guide uses
  [GreenAlgorithms4HPC (GA4HPC)](https://github.com/Cambridge-Sustainable-Computing-Lab/GreenAlgorithms4HPC):
  it's easy to deploy on HPC clusters, supports SLURM, and works
  retrospectively on finished jobs without anything pre-installed.
- Report energy (kWh), CPU time, wall-clock time, memory, and gCO2e for
  representative runs, along with the dataset size and the hardware.
- Optimising the algorithm pays off. In the guide's muvis-align case study,
  stitching a 24.5 TB dataset went from 7.97 kWh / ~1 kgCO2e and 18.3 h to
  1.34 kWh / 183 gCO2e and 8.4 h, through more efficient registration and
  fusion and lower node memory (640 GB → 64 GB). Lowering memory alone
  roughly halved the energy used.

## Resources

- [Introductory guide to green computing for software developers](https://www.software.ac.uk/guide/introductory-guide-green-computing-software-developers)
- [Green Algorithms initiative](https://www.green-algorithms.org/)
- [Green DiSC certification](https://www.software.ac.uk/GreenDiSC)
