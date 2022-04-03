numArgs=$#
binary="${!numArgs}"
output_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ ${numArgs} -eq 0 ]]; then
    echo "Usage: run.sh [options] PATH"
    echo ""
    echo "Required Arguments:"
    echo "  PATH:    Path to elsa's example_argparse binary to use"
    # echo ""
    # echo "Optional Arguments:"
    exit 1
fi

if [[ ! -f "${binary}" || ! -x "${binary}" ]]; then
    echo "Path to binary is not an executable file"
    exit 1
fi

iters=10
size=512
for proj in "Siddon" "Joseph"; do
    echo "====================================================="
    echo "Generating Sinogram for ${proj}"
    echo "====================================================="
    $1 --no-recon --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir}
done

for proj in "Blob" "BSpline"; do
    echo "====================================================="
    echo "Generating sinogram for: ${proj}, and Sinogram Difference image for Joseph and Siddon"
    echo "====================================================="
    $1 --no-recon --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir} --baseline-sinogram "2dsinogram_Siddon.edf" Siddon
    $1 --no-recon --size ${size} --projector ${proj} --phantom SheppLogan --output-dir ${output_dir} --baseline-sinogram "2dsinogram_Joseph.edf" Joseph
done

echo "====================================================="
echo "Generating Sinogram Difference image for Blob to BSpline"
echo "====================================================="
$1 --no-recon --size ${size} --projector Blob --phantom SheppLogan --output-dir ${output_dir} --baseline-sinogram "2dsinogram_BSpline.edf" BSpline

crop_size=$( echo "x = ${size} * 0.25; scale = 0; x / 1" | bc -l)
left_shift=$( echo "x = ${size} * 0.35; scale = 0; x / 1" | bc -l)

for f in *.pgm; do
    # convert pgm to pgn
    convert ./"$f" ./"${f%.pgm}.png"
    # and create a center crop
    convert ./"$f" -gravity center -crop ${crop_size}x${crop_size}-${left_shift}+0 ./"${f%.pgm}_center_crop.png"
done


