import sys
sys.path.insert(0, r'../')
from PDB_file import pdb_file
import argparse

parser = argparse.ArgumentParser(
                    prog = 'PDB charges swapper',
                    description = 'Swap atom charges from one PDB file to another',
                    epilog = 'No more copypasting')

parser.add_argument('-i', '--input',
                    action='store',
                    default=None)
parser.add_argument('-o', '--output',
                    action='store',
                    default="swapped_charges.pdb")
args=parser.parse_args()

pdb1=args.input
output=args.output

pdb1 = pdb_file.PDB_file(pdb1)
output.export_to_pdb(args.output)

