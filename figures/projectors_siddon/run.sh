# Compute forward projections

numArgs=$#
output_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
script_dir=${output_dir}/../../scripts

python ${script_dir}/dda.py ${output_dir}
# python ${script_dir}/dda.py 
