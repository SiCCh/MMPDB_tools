import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pdb_tools import pdb_file
import argparse

parser = argparse.ArgumentParser(
                    prog = 'PDB charges scaler',
                    description = 'Scale atom charges',
                    epilog = 'No more copypasting')

parser.add_argument('-p', '--pdb',
                    action='store',
                    default=None)
parser.add_argument('-s', '--scale',
                    action='store',
                    default=None)
parser.add_argument('-o', '--output',
                    action='store',
                    default=None)
args=parser.parse_args()

pdb=args.inputA
scaling_factor=float(args.scale)
if args.output == None:
    out_name = f"scaled_charges_{scaling_factor}.pdb"
else:
    out_name = args.output

pdb = pdb_file.PDB_file(pdb1)
out = pdb_file.scale_charges(pdb, scaling_factor)
out.export_to_pdb(out_name)


