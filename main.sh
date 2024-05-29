img=$2
 
img_nb=$(printf "%03d" "$img")
 
cp $bin/models/refnerf/"$dataset"/rgb/"$img_nb".png image0.png
cp $bin/models/nrff/"$dataset"/rgb/"$img_nb".png image1.png

python $bin/metrics.py $bin/models/refnerf/"$dataset"/rgb/"$img_nb".png $bin/models/nrff/"$dataset"/rgb/"$img_nb".png ./metrics
