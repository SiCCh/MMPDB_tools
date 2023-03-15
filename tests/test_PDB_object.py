import sys
sys.path.insert(0, r'../')

import PDB_file.pdb_file as pdb_file

pdb = pdb_file.PDB_file("PDB_with_amounts.pdb")
pdb2 = pdb_file.PDB_file("./PFMC_xdraw_type.pdb")
pdb2.describe()