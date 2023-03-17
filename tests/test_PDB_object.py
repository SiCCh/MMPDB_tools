import sys
sys.path.insert(0, r'../')

from PDB_file import pdb_file

pdb = pdb_file.PDB_file("PDB_with_amounts.pdb")
pdb2 = pdb_file.PDB_file("./PFMC_xdraw_type.pdb")
pdb.describe()