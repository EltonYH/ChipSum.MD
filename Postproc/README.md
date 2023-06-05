# Postproc
Some scripts to deal with the problems occur after calculation or simulation, such as the data analyse, plotting graph and so on.

## Functions

### Mean Squared Displacement (MSD)
`MSDVASP.py` is used to calculate MSD from VASP molecular dynamic simulation output file `XDATCAR`.
`MSDQE.py` is used to calculate MSD from QE molecular dynamic simulation output file `.pos`.<br>

   - **Usage:** `python3 MSDVASP.py/MSDQE.py`
   - **Note:** `XDATCAR` file shoule be in the directory. The detials are in the scripts. 

### Bond length
`bond_v2.0.py` is used to calculate and analyze the bond length from `.pos` files obtained from `output_pos.py` script which transforms the VASP molecular dynamic simulation output file `XDATCAR` to `.pos` file using: `python3 output_pos.py`.<br>

   - **Usage:** `python3 bond_v2.0.py ele1 ele2 step0 step1`
   - **Note:** `ele1` and `ele2` are element symblo case-insensitive. `step0` and `step1` are the initial and final MD step to be calculated the bond length. Note that the steps order are reverse, e.g, the `step1=0` means calculation is performed until the final MD step. The detials are in the scripts.

### Fast Fourier Transform (FFT)
`FFT.py` is used to make FFT of atom position from `MSDVASP.py` and `MSDQE.py` output file `.pos`.<br>

### Radial Distribution Function (RDF)
`RDFVASP.py` is used to calculate RDF of pair atoms from `MSDVASP.py` and `MSDQE.py` output file `.pos`.<br>

   - **Usage:** `python3 RDFVASP.py`

### Plot motion trajectory graphs
`plot_trajectory.py` is used to plot motion trajectory graphs of atoms from `MSDVASP.py` and `MSDQE.py` output file `.pos`.<br>

### Spectral Energy Density (SED)
`cal_SED.py` is used to calculate the SED from MD trajectory and then Phonon dispersion and Phonon density of states (DOS).<br>

   - **Note:** Details are in the directory of `Postproc/Spectral_Energy_Density/`
   - **Example:** SWNT

![SWNT](https://github.com/EltonYH/ChipSum.MD/blob/main/Postproc/img/swnt_small.png)<br>

### Velocity Autocorrelation Function (VACF)
The VACF is an important tool to analyze the atom vibrations in the MD simulations. The script `acf_v8.2_noadd0.py` will output the VACF of different atoms seperated by atom ID and three axis. Furthermore, it will also calculated the FFT of VACF and give the Lorentz distribution fitting of it. Besides, the force constants of all the atoms in your system will be also calculated.

   - **Note:** Details are in the directory of `Postproc/Velocity_Autocorrelation_Function/`
