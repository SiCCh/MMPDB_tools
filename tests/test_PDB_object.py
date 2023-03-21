import sys
sys.path.insert(0, r'../')

from pdb_tools import pdb_file

pdb = pdb_file.PDB_file("PDB_with_amounts.pdb")
pdb2 = pdb_file.PDB_file("./PFMC_xdraw_type.pdb")
pdb.describe()
