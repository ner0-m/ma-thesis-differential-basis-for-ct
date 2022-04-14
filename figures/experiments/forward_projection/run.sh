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

# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     echo "====================================================="
#     echo "Generating Sinogram for ${proj} using ${angles} projection positions"
#     echo "====================================================="
#     ${runner} --no-recon --arc 359 --angles ${angles} --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir}
# done

crop_size=$( echo "x = ${size} / 2; scale = 0; x / 1" | bc -l)
left_shift=$( echo "x = ${size} * 0.2; scale = 0; x / 1" | bc -l)
down_shift=$( echo "x = ${size} * 0.68; scale = 0; x / 1" | bc -l)

echo "====================================================="
echo "Generating difference images"
echo "====================================================="
for proj in "Blob" "BSpline"; do
    ${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf" "${output_dir}/2dsinogram_difference_${proj}_Siddon"
    ${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf" "${output_dir}/2dsinogram_difference_${proj}_Joseph"
done
${diff} --normalize "${output_dir}/2dsinogram_Blob.edf" "${output_dir}/2dsinogram_BSpline.edf" "${output_dir}/2dsinogram_difference_Blob_BSpline"

echo "====================================================="
echo "Crop sinogram images and add window colorbar"
echo "====================================================="
for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    convert "${output_dir}/2dsinogram_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dsinogram_cropped_${proj}.png"
    python ../../../scripts/windowed.py 2dsinogram_${proj}.edf
done

echo "====================================================="
echo "Generate crops"
echo "====================================================="
proj="Joseph"
for proj in "Blob" "BSpline"; do
    ${crop} --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_difference_${proj}_Siddon.edf"
    ${crop} --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_difference_${proj}_Joseph.edf"
    mv "${output_dir}/2dsinogram_difference_${proj}_Siddon_cropped.png" "${output_dir}/2dsinogram_cropped_difference_${proj}_Siddon.png"
    mv "${output_dir}/2dsinogram_difference_${proj}_Joseph_cropped.png" "${output_dir}/2dsinogram_cropped_difference_${proj}_Joseph.png"
done
${crop} --width ${crop_size} --height ${crop_size} --padding-top ${down_shift} --padding-left ${left_shift}  "${output_dir}/2dsinogram_difference_Blob_BSpline.edf"
mv "${output_dir}/2dsinogram_difference_Blob_BSpline_cropped.png" "${output_dir}/2dsinogram_cropped_difference_Blob_BSpline.png"

# python ../../../scripts/windowed.py 2dphantom.edf
python ../../../scripts/plot_slice.py 2dsinogram_Blob.edf 2dsinogram_BSpline.edf 2dsinogram_Siddon.edf 2dsinogram_Joseph.edf
python ${rectangle} 2dsinogram_Blob.edf --width ${crop_size} --height ${crop_size} --padding-left ${left_shift} --padding-top ${down_shift}
