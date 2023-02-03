# Velocity Autocorrelation Function (VACF)
The VACF is an important tool to analyze the atom vibrations in the MD simulations. The script `acf_v8.2_noadd0.py` will output the VACF of different atoms seperated by atom ID and three axis. Furthermore, it will also calculated the FFT of VACF and give the Lorentz distribution fitting of it. Besides, the force constants of all the atoms in your system will be also calculated.

## Usage 
```shell
python3 acf_v8.2_noadd0.py dev=0/1/2/3 s=start_MD_step e=end_MD_step step=skip
```
`dev`: 0/1/2/3, the derivation order of trajectory position.<br>
`s, e`: Integer, the initial and end MD steps used to calculate VACF. E.g, if `s=2000`, `e=1000`, the MD trajectorys were extracted as `[-2000, -1000]`.<br>
`step`: Integer, the skip for the extracted MD trajectorys to calculate VACF. E.g, if `step=10`, the extracted MD trajectorys were sampled every 10 MD steps.<br>

## Input 
`POSCAR` apply the lattice paramaters, the type and numbers of the system.<br>
`.pos` apply the absolute Cartesian coordinates each atom in every MD steps, which is the output of `output_pos.py` script.<br>

## Output 
`X_acf_ave.out`: The average VACF of atom X (not normalized).<br>
`X_acf_sum.out`: The normalized VACF of atom X, which is used to calculated pDOS.<br>
`X_pdos.out`: The pDOS data of atom X.<br>
`Total_DOS.out`: The total phonon DOS of this system, which is calculated by the mass weighted average of the pDOS of each atom.<br>
`Force_constant_s_e.log`: The Force constant for each atom type in the system, which is calcualted by the integral of `E^2*pDOS`.<br>


## Note 
1. It is suggested to use `acf_v8.2_noadd0.py` after `output_pos.py`
2. The script `output_pos.py` is to seperate the XDATCAR by different atoms and the positions are converted to absolute Cartesian coordinates.

