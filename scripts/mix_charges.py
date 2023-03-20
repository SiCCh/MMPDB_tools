import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PDB_file import pdb_file
import argparse

parser = argparse.ArgumentParser(
                    prog = 'PDB charges mixer',
                    description = 'Mix atom charges from two PDB files. New charges = pdb1*mixing_factor + pdb2*(1-mixing_factor)',
                    epilog = 'No more copypasting')

parser.add_argument('-a', '--inputA',
                    action='store',
                    default=None)
parser.add_argument('-b', '--inputB',
                    action='store',
                    default=None)
parser.add_argument('-s', '--mix',
                    action='store',
                    default=0.5)
parser.add_argument('-o', '--output',
                    action='store',
                    default="swapped_charges.pdb")
args=parser.parse_args()

pdb1=args.inputA
pdb2=args.inputB
mixing_factor=float(args.mix)

pdb1 = pdb_file.PDB_file(pdb1)
pdb2 = pdb_file.PDB_file(pdb2)
output = pdb_file.mix_charges(pdb1, pdb2, mixing_factor)
output.export_to_pdb(args.output)


