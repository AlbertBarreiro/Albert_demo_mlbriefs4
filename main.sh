img=$2
 
img_nb=$(printf "%03d" "$img")
 
cp $bin/models/refnerf/"$dataset"/rgb/"$img_nb".png image0.png
cp $bin/models/nrff/"$dataset"/rgb/"$img_nb".png image1.png
cp $bin/models/nrff/"$dataset"/rgb/"$img_nb".png gt.png

python $bin/metrics.py image0.png gt.png ./metrics
