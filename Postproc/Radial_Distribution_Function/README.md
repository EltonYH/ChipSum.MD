# Radial Distribution Function (RDF)
Scripts are used to calculate RDF of pair atoms from `output_pos.py` output file `.pos`. The directory of `vasp/` is for VASP output file `XDATCAR` and `qe` id for QE output file `.pos`.

## VASP
### Version 1.0
  - **Usage:** `python3 RDFVASP.py`

### Version 2.0
  - **Usage:** `python3 RDFVASP.py`
  - **Modify:** The script was updated in some aspects, however, the input files `.pos` and elements names should be modified in the script.

### Version 3.0
  - **Usage:** `python3 RDFVASP.py ele1 ele2`
  - **Modify:** The script was modified to use much easier. You need not modify the script every time before you use it. Besides, the script has been modified to adopt all the crystal systems.

## QE
### Version 1.0
  - **Usage:** `python3 RDFQE.py`
