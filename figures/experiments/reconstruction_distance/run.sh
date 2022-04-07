# Reconstruction with different differences

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
echo "Projector;Distance;MSR;RMSR;MAE;PSNR;SSIM;" > "metrics.csv"

iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-128}"

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    for dist in 1 10 50 100 200; do
        echo "====================================================="
        echo "Reconstruction Rectangle using ${proj} projector with distance ${dist}"
        echo "====================================================="
        ${runner} --distance ${dist} --iters ${iters} --size ${size} --projector ${proj} --solver FISTA --output-dir ${output_dir} --analyze | tee ${proj}.log

        # extract error metrics from log
        mse=$(cat "${proj}.log" | grep -oh "\sMSE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
        rmse=$(cat "${proj}.log" | grep -oh "\sRMSE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
        mae=$(cat "${proj}.log" | grep -oh "\sMAE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
        psnr=$(cat "${proj}.log" | grep -oh "\sPSNR:\s[0-9]*[.][0-9]*" | cut -d: -f2 | xargs)
        ssim=$(cat "${proj}.log" | grep -oh "\sSSIM:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)

        mv 2ddifference_${proj}.pgm 2ddifference_${dist}_${proj}.pgm
        mv 2ddifference_${proj}.edf 2ddifference_${dist}_${proj}.edf
        mv 2dreconstruction_${proj}.pgm 2dreconstruction_${dist}_${proj}.pgm
        mv 2dreconstruction_${proj}.edf 2dreconstruction_${dist}_${proj}.edf
        mv 2dsinogram_${proj}.pgm 2dsinogram_${dist}_${proj}.pgm
        mv 2dsinogram_${proj}.edf 2dsinogram_${dist}_${proj}.edf

        # write error metrics it to file
        printf "${proj};${dist}${mse};${rmse};${mae};${psnr};${ssim}\n" >> "metrics.csv"
    done
done

printf "Converting pgm files to pgn.."
for f in *.pgm; do
    # convert pgm to pgn
    convert ./"$f" ./"${f%.pgm}.png"
done
printf "done\n"
echo "====================================================="
