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

iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-128}"

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    echo "====================================================="
    echo "Reconstruction Rectangle using ${proj} projector"
    echo "====================================================="
    ${runner} --dims 3 --iters ${iters} --size ${size} --projector ${proj} --solver FISTA --output-dir ${output_dir} --analyze | tee ${proj}.log

    # extract error metrics from log
    mse=$(cat "${proj}.log" | grep -oh "\sMSE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
    rmse=$(cat "${proj}.log" | grep -oh "\sRMSE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
    mae=$(cat "${proj}.log" | grep -oh "\sMAE:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)
    psnr=$(cat "${proj}.log" | grep -oh "\sPSNR:\s[0-9]*[.][0-9]*" | cut -d: -f2 | xargs)
    ssim=$(cat "${proj}.log" | grep -oh "\sSSIM:\s[0-9]*[.][0-9]*$" | cut -d: -f2 | xargs)

    # write error metrics it to file
    printf "${proj};${mse};${rmse};${mae};${psnr};${ssim}\n" >> "metrics.csv"
done

echo "====================================================="
printf "Creating difference between Blob and B-Spline projector"
${diff} "${output_dir}/2dreconstruction_Blob.edf" "${output_dir}/2dreconstruction_BSpline.edf" "${output_dir}/2ddifference_Blob_BSpline"
printf "done\n"

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
for f in 2dreconstruction_{Blob,BSpline,Siddon,Joseph}.pgm 2ddifference_{Blob,BSpline,Siddon,Joseph}.pgm 2ddifference_Blob_BSpline.pgm; do
    convert ./"$f" -gravity center -crop ${crop_size}x${crop_size}-${left_shift}-${left_shift} ./"${f%.pgm}_croped.png"
done
printf "done\n"
echo "====================================================="
