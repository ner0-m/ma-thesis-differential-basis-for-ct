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
size="${RUN_SIZE:-256}"
angles_default=$( echo "x = ${size} * 1.5; scale = 0; x / 1;" | bc -l)
angles="${RUN_ANGLES:-${angles_default}}"

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    echo "====================================================="
    echo "Generating Sinogram for ${proj} using ${angles} projection positions"
    echo "====================================================="
    ${runner} --no-recon --angles ${angles} --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir}
done

echo "====================================================="
echo "Generating difference images"
echo "====================================================="
proj="Blob"
${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf"
${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf"

proj="BSpline"
${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf"
${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf"
${diff} --normalize "${output_dir}/2dsinogram_Blob.edf" "${output_dir}/2dsinogram_BSpline.edf"

crop_size=$( echo "x = ${size} / 2; scale = 0; x / 1" | bc -l)
left_shift=$( echo "x = ${size} * 0.2; scale = 0; x / 1" | bc -l)
down_shift=$( echo "x = ${size} * 0.68; scale = 0; x / 1" | bc -l)

for f in *.pgm; do
    # convert pgm to pgn
    convert "$f" "${f%.pgm}.png"
done

echo "====================================================="
echo "Add window colorbar to sinogram images"
echo "====================================================="
for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    # and create a center crop
    convert "${output_dir}/2dsinogram_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dsinogram_croped_${proj}.png"
    python ../../../scripts/windowed.py 2dsinogram_${proj}.edf
done

echo "====================================================="
echo "Generate crops"
echo "====================================================="
proj="Joseph"
convert "${output_dir}/2dsinogram_difference_Blob_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dsinogram_croped_difference_Blob_${proj}.png"
convert "${output_dir}/2dsinogram_difference_BSpline_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dsinogram_croped_difference_BSpline_${proj}.png"
proj="Siddon"
convert "${output_dir}/2dsinogram_difference_Blob_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dsinogram_croped_difference_Blob_${proj}.png"
convert "${output_dir}/2dsinogram_difference_BSpline_${proj}.png" -crop ${crop_size}x${crop_size}+${left_shift}+${down_shift} "2dsinogram_croped_difference_BSpline_${proj}.png"

python ../../../scripts/windowed.py 2dphantom.edf
python ../../../scripts/plot_slice.py 2dsinogram_*.edf
python ${rectangle} 2dsinogram_Blob.edf --width ${crop_size} --height ${crop_size} --padding-left ${left_shift} --padding-top ${down_shift}
