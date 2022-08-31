# Mean Squared Displacement (MSD)
MSD is one of the most important properties of Molecular Dynamic (MD) simulation. The diffusion coefficient could be obtained directly from MSD. The directory `VASP/` cotains the scripts for VASP MD output file `XDATCAR` and the `QE/` is for QE MD output file `.pos`.

## VASP
### Version 1.0
  - **Usage:** `python3 MSDVASP.py`
  - **Properties:** This Version could deal with one `XDATCAR` file, and the atom positions are divided in different files with name of `element.pos`.
  
### Version 2.0


## QE
### Version 1.0
  - **Usage:** `python3 MSDQE.py`
  - **Properties:** This Version could deal with one `.pos` file, and the atom positions are divided in different files with name of `element.pos`.

