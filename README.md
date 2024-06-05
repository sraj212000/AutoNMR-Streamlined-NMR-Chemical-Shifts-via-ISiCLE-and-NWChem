# AutoNMR-Streamlined-NMR-Chemical-Shifts-via-ISiCLE-and-NWChem
This repository aims to design and implement an automated workflow to streamline NMR chemical shift calculations using [NWChem](https://www.nwchem-sw.org/). It also involves developing a user-friendly Python API to define molecular systems and specify NMR parameters, simplifying the process and making it more efficient for researchers.

### The primary objectives of this repository are as follows:
- Design and implementation of an automated workflow that streamlines the process of NMR chemical shift calculations using [NWChem](https://www.nwchem-sw.org/)
- Development of a user-friendly [Python](https://www.python.org/) API (Application Programming Interface) for molecular system definition and NMR parameter specification

### What Is NMR Chemical Shift ?
In NMR (Nuclear Magnetic Resonance) spectroscopy, chemical shifts denote the variations in the resonant frequency of a nucleus within a magnetic field, induced by its surrounding chemical environment. These variations arise from the shielding or deshielding effects exerted by the electron cloud around the nucleus. Local electron density variations, influenced by adjacent atoms or functional groups, modify the resonant frequency of the nucleus relative to a reference standard, typically tetramethylsilane (TMS) in organic solvents. This modification, quantified in parts per million (ppm), is termed the chemical shift. TMS, or (CH₃)₄Si, serves as the standard reference for chemical shifts, with δTMS defined as 0 ppm. Chemical shift measurements for ¹H nuclei in samples are referenced against the ¹H resonance of TMS. Grasping the trends in chemical shifts is essential for accurate NMR spectral interpretation. For more details you can visit here [Chemical Shift](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_(Morsch_et_al.)/13%3A_Structure_Determination_-_Nuclear_Magnetic_Resonance_Spectroscopy/13.03%3A_Chemical_Shifts_in_H_NMR__Spectroscopy)

## Getting Started with NWChem
NWChem aims to provide its users with computational chemistry tools that are scalable both in their ability to treat large scientific computational chemistry problems efficiently, and in their use of available parallel computing resources from high-performance parallel supercomputers to conventional workstation clusters.

NWChem software can handle:

 - Biomolecules, nanostructures, and solid-state
 - From quantum to classical, and all combinations
 - Ground and excited-states
 - Gaussian basis functions or plane-waves
 - Scaling from one to thousands of processors
 - Properties and relativistic effects
   
NWChem consists of independent modules that perform the various functions of the code. Examples of modules include the input parser, SCF energy, SCF analytic gradient, DFT energy, etc.. For details about the NWChem you can visit the NWChem [Documentation Page](https://nwchemgit.github.io/Compiling-NWChem.html) here.
