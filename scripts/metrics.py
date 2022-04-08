#!/usr/bin/env python

import argparse
from pathlib import Path

from skimage.metrics import structural_similarity 
from skimage.metrics import mean_squared_error
from skimage.metrics import normalized_root_mse
from skimage.metrics import peak_signal_noise_ratio

parser = argparse.ArgumentParser(description="Read file and crop into given section")
parser.add_argument("phantom", type=Path, help="Path to edf file to be windowed")
parser.add_argument("reconstruction", type=Path, help="Path to edf file to be windowed")

args = parser.parse_args()

if __name__ == "__main__":
    phantom_path = args.phantom
    reconstruction_path = args.reconstruction
    import edf

    phantom = edf.readedf(phantom_path)
    reconstruction = edf.readedf(reconstruction_path)

    MSE = mean_squared_error(phantom, reconstruction)
    NRMSE = normalized_root_mse(phantom, reconstruction)
    # PSNR = peak_signal_noise_ratio(phantom, reconstruction, data_range=phantom.max() - phantom.min())
    PSNR = peak_signal_noise_ratio(phantom, reconstruction)
    SSIM = structural_similarity(phantom, reconstruction, data_range=phantom.max() - phantom.min())

    # print(f"TEST: {MSE = }, {NRMSE = }, {PSNR = }, {SSIM = }")
    print(f"{MSE = :.3e}, {NRMSE = :.3e}, {PSNR = :4.3F}, {SSIM = :4.3F}")
