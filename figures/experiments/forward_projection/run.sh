# Compute forward projections

numArgs=$#
elsa_dir="${!numArgs}"
output_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

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
diff=${elsa_dir}bin/examples/example_difference

iters="${RUN_ITERS:-25}"
size="${RUN_SIZE:-128}"
angles_default=$( echo "x = ${size} * 1.5; scale = 0; x / 1;" | bc -l)
angles="${RUN_ANGLES:-${angles_default}}"

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    echo "====================================================="
    echo "Generating Sinogram for ${proj} using ${angles} projection positions"
    echo "====================================================="
    ${runner} --no-recon --angles ${angles} --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir}
done

# TODO: Maybe stay consistent and nromalize everything?
# for proj in "Blob" "BSpline"; do
#     echo "====================================================="
#     echo "Generating sinogram for: ${proj}, and Sinogram Difference image for Joseph and Siddon"
#     echo "====================================================="
#     ${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf" "${output_dir}/2dsinodifference_${proj}_Siddon"
#     ${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf" "${output_dir}/2dsinodifference_${proj}_Joseph"
# done
proj="Blob"
echo "====================================================="
echo "Generating sinogram for: ${proj}, and Sinogram Difference image for Joseph and Siddon"
echo "====================================================="
${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf" "${output_dir}/2dsinodifference_${proj}_Siddon"
${diff} --normalize "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf" "${output_dir}/2dsinodifference_${proj}_Joseph"

proj="BSpline"
echo "====================================================="
echo "Generating sinogram for: ${proj}, and Sinogram Difference image for Joseph and Siddon"
echo "====================================================="
${diff} "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Siddon.edf" "${output_dir}/2dsinodifference_${proj}_Siddon"
${diff} "${output_dir}/2dsinogram_${proj}.edf" "${output_dir}/2dsinogram_Joseph.edf" "${output_dir}/2dsinodifference_${proj}_Joseph"

echo "====================================================="
echo "Generating Sinogram Difference image for Blob to BSpline"
echo "====================================================="
${diff} --normalize "${output_dir}/2dsinogram_Blob.edf" "${output_dir}/2dsinogram_BSpline.edf" "${output_dir}/2dsinodifference_Blob_BSpline"

crop_size=$( echo "x = ${size} * 0.25; scale = 0; x / 1" | bc -l)
left_shift=$( echo "x = ${size} * 0.35; scale = 0; x / 1" | bc -l)

for f in *.pgm; do
    # convert pgm to pgn
    convert "$f" "${f%.pgm}.png"
done

for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
    # and create a center crop
    convert "${output_dir}/2dsinogram_${proj}.png" -gravity center -crop ${crop_size}x${crop_size}-${left_shift}+0 "2dsinogram_croped_${proj}.png"
done
