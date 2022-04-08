# Reconstruction triangle

numArgs=$#
elsa_dir="${!numArgs}"
output_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
script_dir=${output_dir}/../../../scripts

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
rectangle=${script_dir}/rectangle.py
metrics=${script_dir}/metrics.py

# setup csv log file for error metrics data
touch "metrics.csv"
echo "Projector;MSE;NRMSE;PSNR;SSIM" > "metrics.csv"

iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-256}"

# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     echo "====================================================="
#     echo "Reconstruction Rectangle using ${proj} projector"
#     echo "====================================================="
#     ${runner} --iters ${iters} --size ${size} --projector ${proj} --solver FISTA --phantom Rectangle --output-dir ${output_dir} --analyze | tee ${proj}.log
# done

echo "====================================================="
# printf "Creating difference between Blob and B-Spline projector"
# ${diff} "${output_dir}/2dreconstruction_Blob.edf" "${output_dir}/2dreconstruction_BSpline.edf" "${output_dir}/2ddifference_Blob_BSpline"
# printf "done\n"

echo "====================================================="

# printf "Converting pgm files to png..."
# for f in *.pgm; do
#     # convert pgm to pgn
#     convert ./"$f" ./"${f%.pgm}.png"
# done
# printf "done\n"

# crop_size=$( echo "x = ${size} * 0.45; scale = 0; x / 1" | bc -l)
# left_shift=$( echo "x = ${size} * 0.15; scale = 0; x / 1" | bc -l)

# printf "Creating croped images..."
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     # and create a center crop
#     convert "${output_dir}/2dreconstruction_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dreconstruction_croped_${proj}.png"
#     python ../../../scripts/windowed.py 2dreconstruction_${proj}.edf
# done

# printf "done\n"
# echo "====================================================="
# python ../../../scripts/windowed.py 2dphantom.edf
# python ${rectangle} 2dphantom.edf --width ${crop_size} --height ${crop_size} --padding-left ${left_shift} --padding-top ${left_shift}

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    python ${metrics} 2dphantom.edf 2dreconstruction_${proj}.edf | tee ${proj}.log

    # extract error metrics from log
    mse=$(cat "${proj}.log" | grep -oh "^MSE\s=\s[0-9]*[\.][0-9]*e[-|+][0-9]*" | cut -d= -f2 | xargs)
    rmse=$(cat "${proj}.log" | grep -oh "NRMSE\s=\s[0-9]*[\.][0-9]*e[-|+][0-9]*" | cut -d= -f2 | xargs)
    psnr=$(cat "${proj}.log" | grep -oh "PSNR\s=\s[0-9]*[.][0-9]*" | cut -d= -f2 | xargs)
    ssim=$(cat "${proj}.log" | grep -oh "SSIM\s=\s[0-9]*[.][0-9]*$" | cut -d= -f2 | xargs)

    # write error metrics it to file
    if [[ "${proj}" = "BSpline" ]]; then
        printf "B-Spline;${mse};${rmse};${psnr};${ssim}\n" >> "metrics.csv"
    else
        printf "${proj};${mse};${rmse};${psnr};${ssim}\n" >> "metrics.csv"
    fi
done
