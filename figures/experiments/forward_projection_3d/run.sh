# 3D Shepp-Logan Reconstruction 

numArgs=$#
elsa_dir="${!numArgs}"
output_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ ${numArgs} -eq 0 ]]; then
    echo "Usage: run.sh [options] PATH"
    echo ""
    echo "Required Arguments:"
    echo "  PATH:    Path to build directory of elsa"
    exit 1
fi

if [[ ! -d "${elsa_dir}" ]]; then
    echo "Provide path to elsa's build directory as last argument"
    exit 1
fi

runner=${elsa_dir}bin/examples/example_argparse
diff=${elsa_dir}bin/examples/example_difference

# setup csv log file for error metrics data
touch "metrics.csv"
echo "Projector;MSR;RMSR;MAE;PSNR;SSIM" > "metrics.csv"

size="${RUN_SIZE:-256}"
angles_default=$( echo "x = ${size} * 1.5; scale = 0; x / 1;" | bc -l)
angles="${RUN_ANGLES:-${angles_default}}"

# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     echo "====================================================="
#     echo "Reconstruction Rectangle using ${proj} projector"
#     echo "====================================================="
#     ${runner} --dims 3 --arc 360 --phantom SheppLogan --angles ${angles} --size ${size} --projector ${proj} --no-recon --output-dir ${output_dir} --analyze | tee ${proj}.log
# done

printf "Converting pgm files to png.."
for f in *.pgm; do
    # convert pgm to pgn
    convert ./"$f" ./"${f%.pgm}.png"
done
printf "done\n"
