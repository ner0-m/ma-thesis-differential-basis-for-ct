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

iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-128}"

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    echo "====================================================="
    echo "Producing output for artifacts for projector: ${proj}"
    echo "====================================================="
    ${runner} --iters ${iters} --size ${size} --projector ${proj} --solver FISTA --phantom SheppLogan --output-dir ${output_dir} --analyze | tee "${proj}.log"

    # extract error metrics from log
    mse=$(cat "${proj}.log" | grep -oh "\sMSE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
    rmse=$(cat "${proj}.log" | grep -oh "\sRMSE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
    mae=$(cat "${proj}.log" | grep -oh "\sMAE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
    psnr=$(cat "${proj}.log" | grep -oh "\sPSNR:\s[0-9]*[.][0-9]*" | cut -d: -f2 | xargs)
    ssim=$(cat "${proj}.log" | grep -oh "\sSSIM:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)

    # write error metrics it to file
    printf "${proj};${mse};${rmse};${mae};${psnr};${ssim}\n" >> "metrics.csv"
done

# convert pgm to png for consumption in latex
for f in *.pgm; do
    convert ./"$f" ./"${f%.pgm}.png"
done

crop_size=$( echo "x = ${size} * 0.6; scale = 0; x / 1" | bc -l)

# and create a center crop
for f in 2dreconstruction_{Blob,BSpline,Siddon,Joseph}.pgm; do
    convert ./"$f" -gravity center -crop ${crop_size}x${crop_size}+${left_shift}+0 ./"${f%.pgm}_center_crop.png"
done


