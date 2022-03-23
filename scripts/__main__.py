import argparse
from pathlib import Path
 
parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument("--figure-path", type=Path)
parser.add_argument("--all", default=True)

import pylib.tesis.basis.bspline_coeffs as bspline_coeffs
import pylib.tesis.basis.bspline_basis as bspline_basis
import pylib.tesis.basis.pixel_coeffs as pixel_coeffs

def main():
    args = parser.parse_args()
    bspline_coeffs.gen_fig_bspline_transformation(args.figure_path)
    pixel_coeffs.gen_fig_bspline_transformation(args.figure_path)


if __name__ == "__main__":
    main()
