dataset=$1
img=$2
 
cp $bin/models/refnerf/"$dataset"/rgb/"$img".png image0.png
cp $bin/models/nrff/"$dataset"/rgb/"$img".png image1.png