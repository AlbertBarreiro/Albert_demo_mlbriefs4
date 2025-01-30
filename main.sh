dataset=$(cat $input_0)
az=$1


if [[ "$dataset" != "toaster" && "$dataset" != "ani" && "$dataset" != "ball" ]]; then
    echo "Choose between the three different availabe datasets."
    exit 1
fi




python  $bin/find_demo_images.py $bin/models/refnerf/"$dataset"/transforms_demo_ipol.json $az $bin

gt_rgb=demo_output/gt_rgb/c_view.png
refnerf_rgb=demo_output/refnerf_rgb/c_view.png
nrff_rgb=demo_output/nrff_rgb/c_view.png
convert $gt_rgb -resize 50% $gt_rgb

python $bin/metrics.py $gt_rgb $refnerf_rgb ./metrics_refnerf
python $bin/metrics.py $gt_rgb $nrff_rgb ./metrics_nrff


echo "Correct execution"
