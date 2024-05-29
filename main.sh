dataset=$(cat $input_0)
img=$2
 
img_nb=$(printf "%03d" "$img")
img_nb4=$(printf "%04d" "$img")
 
cp $bin/models/refnerf/"$dataset"/rgb/"$img_nb".png image0.png
cp $bin/models/nrff/"$dataset"/rgb/"$img_nb".png image1.png
cp $bin/models/gt/"$dataset"/rgb/"$img_nb4".png image2.png


python $bin/metrics.py image0.png image2.png ./metrics_refnerf

python $bin/metrics.py image1.png image2.png ./metrics_nrff