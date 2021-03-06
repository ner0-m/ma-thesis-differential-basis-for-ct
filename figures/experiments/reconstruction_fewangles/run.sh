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
metrics=${script_dir}/metrics.py

# setup csv log file for error metrics data
touch "metrics.csv"
echo "Projector;MSE;NRMSE;PSNR;SSIM" > "metrics.csv"

iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-128}"
angles=$( echo "x = ${size} * 0.1; scale = 0; x / 1" | bc -l)

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    echo "====================================================="
    echo "Reconstruction Rectangle using ${proj} projector"
    echo "====================================================="
    ${runner} --angles ${angles} --arc 179 --iters ${iters} --size ${size} --projector ${proj} --solver FISTA --output-dir ${output_dir} --analyze | tee ${proj}.log
done

echo "====================================================="
printf "Converting pgm files to pgn.."
for f in *.pgm; do
    # convert pgm to pgn
    convert ./"$f" ./"${f%.pgm}.png"
done
printf "done\n"

crop_size=$( echo "x = ${size} * 0.45; scale = 0; x / 1" | bc -l)
left_shift=$( echo "x = ${size} * 0.15; scale = 0; x / 1" | bc -l)

printf "Creating croped images"
# create a crop
for f in 2dreconstruction_{Blob,BSpline,Siddon,Joseph}.pgm 2ddifference_{Blob,BSpline,Siddon,Joseph}.pgm; do
    convert ./"$f" -gravity center -crop ${crop_size}x${crop_size}-${left_shift}-${left_shift} ./"${f%.pgm}_croped.png"
done
printf "done\n"
echo "====================================================="

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
