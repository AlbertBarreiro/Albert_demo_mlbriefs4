dataset=$(cat $input_0)
az=$1


if [[ "$dataset" != "toaster" && "$dataset" != "ani" && "$dataset" != "ball" ]]; then
    echo "Choose between the three different availabe datasets."
    exit 1
fi




python  $bin/find_demo_images.py $bin/models/gt/"$dataset"/transforms_demo_ipol.json $dataset $az $bin

gt_rgb=demo_output/gt_rgb/r_view.png
convert $gt_rgb -resize 50% $gt_rgb
gt_rgb=demo_output/gt_rgb/l_view.png
convert $gt_rgb -resize 50% $gt_rgb
gt_rgb=demo_output/gt_rgb/merged_image.png
convert $gt_rgb -resize 50% $gt_rgb
gt_rgb=demo_output/gt_rgb/c_view.png
convert $gt_rgb -resize 50% $gt_rgb

python $bin/metrics.py $gt_rgb demo_output/refnerf_rgb/c_view.png ./metrics_refnerf
python $bin/metrics.py $gt_rgb demo_output/nrff_rgb/c_view.png ./metrics_nrff



view2display=merged_image.png
refnerf_rgb=demo_output/refnerf_rgb/$view2display
nrff_rgb=demo_output/nrff_rgb/$view2display
gt_rgb=demo_output/gt_rgb/$view2display



echo "Correct execution"
