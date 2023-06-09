import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pdb_tools import pdb_file
import argparse

parser = argparse.ArgumentParser(
                    prog = 'PDB charges swapper',
                    description = 'Swap atom charges from one PDB file to another',
                    epilog = 'No more copypasting')

parser.add_argument('-a', '--inputA',
                    action='store',
                    default=None)
parser.add_argument('-b', '--inputB',
                    action='store',
                    default=None)
parser.add_argument('-o', '--output',
                    action='store',
                    default="swapped_charges.pdb")
args=parser.parse_args()

pdb1=args.inputA
pdb2=args.inputB

pdb1 = pdb_file.PDB_file(pdb1)
pdb2 = pdb_file.PDB_file(pdb2)
out = pdb_file.swap_charges(pdb1, pdb2)
out.export_to_pdb(args.output)


