dataset=$(cat $input_0)
img=$2
 
img_nb=$(printf "%03d" "$img")
img_nb4=$(printf "%04d" "$img")
 
cp $bin/models/refnerf/"$dataset"/rgb/"$img_nb".png image0.png
cp $bin/models/nrff/"$dataset"/rgb/"$img_nb".png image1.png

cp $bin/models/gt/"$dataset"/rgb/"$img_nb4".png image2.png

# Get the original dimensions
width=$(identify -format "%w" image2.png)
height=$(identify -format "%h" image2.png)

# Calculate new dimensions
new_width=$((width / 2))
new_height=$((height / 2))

# Downscale the image to exact dimensions
convert image2.png -resize "${new_width}x${new_height}" image2.png


cp $bin/models/refnerf/"$dataset"/normals/"$img_nb".png normals_refnerf.png
cp $bin/models/nrff/"$dataset"/normals/"$img_nb".png normals_nrff.png


python $bin/metrics.py image2.png image0.png ./metrics_refnerf

python $bin/metrics.py image2.png image1.png ./metrics_nrff

echo "Correct execution"
