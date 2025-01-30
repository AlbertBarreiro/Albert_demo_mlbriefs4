dataset=$(cat $input_0)
az=$1


if [[ "$dataset" != "toaster" && "$dataset" != "ani" && "$dataset" != "ball" ]]; then
    echo "Choose between the three different availabe datasets."
    exit 1
fi




python  $bin/find_demo_images.py $bin/models/gt/"$dataset"/transforms_demo_ipol.json $dataset $az $bin

gt_rgb=demo_output/gt_rgb/c_view.png
convert $gt_rgb -resize 50% $gt_rgb
gt_rgb=demo_output/gt_rgb/l_view.png
convert $gt_rgb -resize 50% $gt_rgb
gt_rgb=demo_output/gt_rgb/r_view.png
convert $gt_rgb -resize 50% $gt_rgb

tmpdir=demo_output/gt_rgb
convert +append $tmp_dir/l_view.png $tmp_dir/c_view.png $tmp_dir/r_view.png $tmp_dir/merged_image.png
tmpdir=demo_output/refnerf_rgb
convert +append $tmp_dir/l_view.png $tmp_dir/c_view.png $tmp_dir/r_view.png $tmp_dir/merged_image.png
tmpdir=demo_output/nrff_rgb
convert +append $tmp_dir/l_view.png $tmp_dir/c_view.png $tmp_dir/r_view.png $tmp_dir/merged_image.png
tmpdir=demo_output/nrff_normals
convert +append $tmp_dir/l_view.png $tmp_dir/c_view.png $tmp_dir/r_view.png $tmp_dir/merged_image.png
tmpdir=demo_output/refnerf_normals
convert +append $tmp_dir/l_view.png $tmp_dir/c_view.png $tmp_dir/r_view.png $tmp_dir/merged_image.png

view2display=merged_image.png
refnerf_rgb=demo_output/refnerf_rgb/$view2display
nrff_rgb=demo_output/nrff_rgb/$view2display
gt_rgb=demo_output/gt_rgb/$view2display

python $bin/metrics.py $gt_rgb $refnerf_rgb ./metrics_refnerf
python $bin/metrics.py $gt_rgb $nrff_rgb ./metrics_nrff


echo "Correct execution"
