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
diff=${script_dir}/diff.py
rectangle=${script_dir}/rectangle.py
metrics=${script_dir}/metrics.py
crop=${script_dir}/crop.py
windowed=${script_dir}/windowed.py

# setup csv log file for error metrics data
touch "metrics.csv"
echo "Projector;MSE;NRMSE;PSNR;SSIM" > "metrics.csv"

iters="${RUN_ITERS:-300}"
size="${RUN_SIZE:-512}"

phantom="abdomen"
# for proj in "Siddon" "Joseph" "Blob" "BSpline"; do
#     echo "====================================================="
#     echo "Reconstruction Rectangle using ${proj} projector, with lambda ${lambda}"
#     echo "====================================================="
#     ${runner} --input "${output_dir}/${phantom}_${size}.edf" --arc 180 --iters ${iters} --projector ${proj} --solver FISTA --output-dir ${output_dir} --analyze | tee ${proj}.log
# done

crop_size=$( echo "x = ${size} * 0.45; scale = 0; x / 1" | bc -l)
down_shift=$( echo "x = ${size} * 0.15; scale = 0; x / 1" | bc -l)
left_shift=$( echo "x = ${size} * 0.3; scale = 0; x / 1" | bc -l)

# printf "Convert phantom to png..."
# convert "${output_dir}/2dphantom.pgm" "${output_dir}/2dphantom.png"
# printf "done\n"
#
# printf "Creating difference images..."
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     # and create a center crop
#     ${diff} "${output_dir}/2dphantom.edf" "${output_dir}/2dreconstruction_${proj}.edf" "${output_dir}/2dreconstruction_difference_${proj}"
# done
# printf "done\n"
#
# printf "Creating cropped images of reconstruction..."
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     ${crop} --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dreconstruction_${proj}.edf"
#
#     # Move to better namming
#     mv "${output_dir}/2dreconstruction_${proj}_cropped.png" "${output_dir}/2dreconstruction_cropped_${proj}.png"
# done
# printf "done\n"
#
# printf "Creating cropped images of difference images..."
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     ${crop} --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dreconstruction_difference_${proj}.edf"
#
#     # Move to better namming
#     mv "${output_dir}/2dreconstruction_difference_${proj}_cropped.png" "${output_dir}/2dreconstruction_difference_cropped_${proj}.png"
# done
# printf "done\n"
#
# printf "Overlay red rectangle over phantom..."
# python ${rectangle} "${output_dir}/${phantom}_${size}_normalized.edf" --width ${crop_size} --height ${crop_size} --padding-left ${left_shift} --padding-top ${down_shift}
# printf "done\n"
#
# printf "Add window interval to reconstruction images..."
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     ${windowed} "${output_dir}/2dreconstruction_${proj}.edf"
#
#     # Move to better namming
#     mv "${output_dir}/2dreconstruction_${proj}_windowed.png" "${output_dir}/2dreconstruction_windowed_${proj}.png"
# done
# printf "done\n"
#
# printf "add window interval to reconstruction images..."
# for proj in "blob" "bspline" "siddon" "joseph"; do
#     ${windowed} "${output_dir}/2dreconstruction_difference_${proj}.edf"
#
#     # move to better namming
#     mv "${output_dir}/2dreconstruction_difference_${proj}_windowed.png" "${output_dir}/2dreconstruction_difference_windowed_${proj}.png"
# done
# printf "done\n"
#
# printf "add window interval to cropped difference images..."
# for proj in "blob" "bspline" "siddon" "joseph"; do
#     ${windowed} --padding ${left_shift} ${down_shift} ${crop_size} ${crop_size} "${output_dir}/2dreconstruction_difference_${proj}.edf"
#
#     # move to better namming
#     mv "${output_dir}/2dreconstruction_difference_${proj}_cropped_windowed.png" "${output_dir}/2dreconstruction_difference_cropped_windowed_${proj}.png"
# done
# printf "done\n"
#
# printf "add window interval to cropped reconstruction images..."
# for proj in "blob" "bspline" "siddon" "joseph"; do
#     ${windowed} --padding ${left_shift} ${down_shift} ${crop_size} ${crop_size} "${output_dir}/2dreconstruction_${proj}.edf"
#
#     # move to better namming
#     mv "${output_dir}/2dreconstruction_${proj}_cropped_windowed.png" "${output_dir}/2dreconstruction_cropped_windowed_${proj}.png"
# done
# printf "done\n"

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    python ${metrics} "${output_dir}/${phantom}_${size}_normalized.edf" 2dreconstruction_${proj}.edf | tee ${proj}.log

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
