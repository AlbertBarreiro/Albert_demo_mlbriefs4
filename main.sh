dataset=$(cat $input_0)
img=$1


if [[ "$dataset" != "toaster" && "$dataset" != "ani" && "$dataset" != "ball" ]]; then
    echo "Choose between the three different availabe datasets."
    exit 1
fi


img_nb=$(printf "%03d" "$img")
img_nb4=$(printf "%04d" "$img")

cp $bin/models/refnerf/"$dataset"/rgb/"$img_nb".png image0.png
cp $bin/models/nrff/"$dataset"/rgb/"$img_nb".png image1.png

cp $bin/models/gt/"$dataset"/rgb/"$img_nb4".png image2.png
convert image2.png -resize 50% image2.png

cp $bin/models/refnerf/"$dataset"/normals/"$img_nb".png normals_refnerf.png
cp $bin/models/nrff/"$dataset"/normals/"$img_nb".png normals_nrff.png


python $bin/metrics.py image2.png image0.png ./metrics_refnerf

python $bin/metrics.py image2.png image1.png ./metrics_nrff

echo "Correct execution"
