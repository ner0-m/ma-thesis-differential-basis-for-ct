# Compute forward projections

numArgs=$#
elsa_dir="${!numArgs}"
output_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
script_dir=${output_dir}/../../../scripts

if [[ ${numArgs} -eq 0 ]]; then
    echo "Usage: run.sh [options] PATH"
    echo ""
    echo "Required Arguments:"
    echo "  PATH:    Path to elsa's example_argparse binary to use"
    exit 1
fi

if [[ ! -d "${elsa_dir}" ]]; then
    echo "Provide path to elsa's build directory as last argument"
    exit 1
fi

runner=${elsa_dir}bin/examples/example_argparse
diff=${script_dir}/diff.py
crop=${script_dir}/crop.py
rectangle=${script_dir}/rectangle.py


iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-512}"
angles_default=$( echo "x = ${size} * 1.5; scale = 0; x / 1;" | bc -l)
angles="${RUN_ANGLES:-${angles_default}}"

echo "angles: ${angles}"
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     echo "====================================================="
#     echo "Generating Sinogram for ${proj} using ${angles} projection positions"
#     echo "====================================================="
#     ${runner} --no-recon --arc 359 --angles ${angles} --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir}
# done

# crop_size=$( echo "x = ${size} / 2; scale = 0; x / 1" | bc -l)
# left_shift=$( echo "x = ${size} * 0.2; scale = 0; x / 1" | bc -l)
# down_shift=$( echo "x = ${size} * 0.68; scale = 0; x / 1" | bc -l)
#
# echo "====================================================="
# echo "Generating difference images"
# echo "====================================================="
# for proj in "Blob" "BSpline"; do
#     ${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf" "${output_dir}/2dsinogram_difference_${proj}_Siddon"
#     ${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf" "${output_dir}/2dsinogram_difference_${proj}_Joseph"
# done
# ${diff} --normalize "${output_dir}/2dsinogram_Blob.edf" "${output_dir}/2dsinogram_BSpline.edf" "${output_dir}/2dsinogram_difference_Blob_BSpline"
#
# echo "====================================================="
# echo "Crop sinogram images and add window colorbar"
# echo "====================================================="
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     ${crop} --windowed --from-elsa --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_${proj}.edf"
#     mv "${output_dir}/2dsinogram_${proj}_cropped.png" "${output_dir}/2dsinogram_cropped_${proj}.png"
#     mv "${output_dir}/2dsinogram_${proj}_cropped_windowed.png" "${output_dir}/2dsinogram_cropped_${proj}_windowed.png"
#     python ../../../scripts/windowed.py 2dsinogram_${proj}.edf
# done
#
# echo "====================================================="
# echo "Generate crops for difference"
# echo "====================================================="
# for proj in "Blob" "BSpline"; do
#     ${crop} --windowed --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_difference_${proj}_Siddon.edf"
#     ${crop} --windowed --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_difference_${proj}_Joseph.edf"
#     mv "${output_dir}/2dsinogram_difference_${proj}_Siddon_cropped.png" "${output_dir}/2dsinogram_cropped_difference_${proj}_Siddon.png"
#     mv "${output_dir}/2dsinogram_difference_${proj}_Joseph_cropped.png" "${output_dir}/2dsinogram_cropped_difference_${proj}_Joseph.png"
#
#     mv "${output_dir}/2dsinogram_difference_${proj}_Siddon_cropped_windowed.png" "${output_dir}/2dsinogram_cropped_difference_${proj}_Siddon_windowed.png"
#     mv "${output_dir}/2dsinogram_difference_${proj}_Joseph_cropped_windowed.png" "${output_dir}/2dsinogram_cropped_difference_${proj}_Joseph_windowed.png"
# done
# ${crop} --windowed --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_difference_Blob_BSpline.edf"
# mv "${output_dir}/2dsinogram_difference_Blob_BSpline_cropped.png" "${output_dir}/2dsinogram_cropped_difference_Blob_BSpline.png"
# mv "${output_dir}/2dsinogram_difference_Blob_BSpline_cropped_windowed.png" "${output_dir}/2dsinogram_cropped_difference_Blob_BSpline_windowed.png"

# python ../../../scripts/plot_slice.py  2dsinogram_Blob.edf 2dsinogram_BSpline.edf 2dsinogram_Siddon.edf 2dsinogram_Joseph.edf
# python ../../../scripts/plot_slice.py --slice 288 2dsinogram_Blob.edf 2dsinogram_BSpline.edf
python ../../../scripts/plot_slice.py --slice 96 2dsinogram_Blob.edf 2dsinogram_BSpline.edf
# python ${rectangle} 2dsinogram_Blob.edf --width ${crop_size} --height ${crop_size} --padding-left ${left_shift} --padding-top ${down_shift}
