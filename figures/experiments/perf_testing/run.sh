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

runner=${elsa_dir}bin/examples/example_difference
evaluate=${output_dir}/evaluate.py

angles=512
nruns=50

perf_file="perf_size.csv"
file_3d="perf_3d.csv"
angles_file=perf_angles.csv

# rm -f ${perf_file}
# printf "projector;kind;size;angles;runs;warmups;%s;\n" $(seq -s ';' 1 ${nruns}) > ${perf_file}
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     # for size in  32  38  46  55  67  80  97 116 140 168 203 244 294 353 425 512; do
#     for size in 32 47 70 105 128 256 344 512; do
#         echo "====================================================="
#         printf "Running benchmark for ${proj} of size ${size}\n"
#         echo "====================================================="
#         # Append using tee
#         ${runner} --nruns ${nruns} --size ${size} --projector ${proj} --angles ${angles} ${perf_file}
#     done
# done

# rm -f ${angles_file}
# printf "projector;kind;size;angles;runs;warmups;%s;\n" $(seq -s ';' 1 ${nruns}) > ${angles_file}
# size=128
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     for angles in  32  38  46  55  67  80  97 116 140 168 203 244 294 353 425 512; do
#     # for size in  32  38  46 55 67; do
#         echo "====================================================="
#         printf "Running benchmark for ${proj} of size ${size}\n"
#         echo "====================================================="
#
#         ${runner} --nruns ${nruns} --size ${size} --projector ${proj} --angles ${angles} ${angles_file}
#     done
# done

angles=64
nruns=25
# rm -f ${file_3d}
# printf "projector;kind;size;angles;runs;warmups;%s;\n" $(seq -s ';' 1 ${nruns}) > ${file_3d}
# for proj in "Blob" "BSpline" "Siddon" "Joseph"; do
#     for size in 32 36 42 48 55 64; do
#         echo "====================================================="
#         printf "Running 3D benchmark for ${proj} of size ${size}\n"
#         echo "====================================================="
#         ${runner} --nruns ${nruns} --dims 3 --size ${size} --projector ${proj} --angles ${angles} ${file_3d}
#     done
# done

printf "Generating lineplot for the 2d forward projection..."
python ${evaluate} --lineplot --forward ${perf_file} 2
printf "done\n"
printf "Generating lineplot for the 2d backward projection..."
python ${evaluate} --lineplot --backward ${perf_file} 2
printf "done\n"
printf "Generating lineplot for the 3d forward projection..."
python ${evaluate} --lineplot --forward ${file_3d} 3
printf "done\n"
printf "Generating lineplot for the 3d backward projection..."
python ${evaluate} --lineplot --backward ${file_3d} 3
printf "done\n"
printf "Generating violin plot for the 2d backward projection..."
python ${evaluate} --violinplot --forward ${perf_file} 2
printf "done\n"
printf "Generating violin plot for the 2d backward projection..."
python ${evaluate} --violinplot --backward ${perf_file} 2
printf "done\n"
