import json
import numpy as np
import shutil
import os

def find_demo_images(transforms_path, dataset_id, input_azimuth, bin_path):

    with open(transforms_path, "r") as f:
        data = json.load(f)

    all_azimuths = [x["demo_azimuth"] for x in data["frames"]]
    target_image_idx = all_azimuths.index(str(input_azimuth))
    all_azimuths = [float(x) for x in all_azimuths]
    target_image_path = data["frames"][target_image_idx]["file_path"]
    print(input_azimuth)

    dist_to_other_azimuths = np.array(all_azimuths) - input_azimuth
    neighbor_idx_1, neighbor_idx_2 = np.argsort(abs(dist_to_other_azimuths))[1:3]
    dist_to_neighbor1 = dist_to_other_azimuths[neighbor_idx_1]
    dist_to_neighbor2 = dist_to_other_azimuths[neighbor_idx_2]
    print(dist_to_neighbor1, dist_to_neighbor2)

    neighbor_path_1 = data["frames"][neighbor_idx_1]["file_path"]
    neighbor_path_2 = data["frames"][neighbor_idx_2]["file_path"]

    if dist_to_neighbor1 < dist_to_neighbor2:
        output_paths = (neighbor_path_1, target_image_path, neighbor_path_2)
    else:
        output_paths = (neighbor_path_2, target_image_path, neighbor_path_1)

    
    format_filename4 = lambda p : f"{int(os.path.basename(p).split('_')[-1]):04d}.png"
    format_filename3 = lambda p : f"{int(os.path.basename(p).split('_')[-1]):03d}.png"

    gt_rgb = [f"{bin_path}/models/gt/{dataset_id}/rgb/{format_filename4(p)}" for p in output_paths]
    nrff_rgb = [f"{bin_path}/models/nrff/{dataset_id}/rgb/{format_filename3(p)}" for p in output_paths]
    refnerf_rgb = [f"{bin_path}/models/refnerf/{dataset_id}/rgb/{format_filename3(p)}" for p in output_paths]

    nrff_normals= [f"{bin_path}/models/nrff/{dataset_id}/rgb/{format_filename3(p)}" for p in output_paths]
    refnerf_normals = [f"{bin_path}/models/refnerf/{dataset_id}/rgb/{format_filename3(p)}" for p in output_paths]


    # WRITE RGB IMAGES
    os.makedirs("demo_output/gt_rgb", exist_ok=True)
    for source_path, target_path in zip(gt_rgb, ["l_view.png", "c_view.png", "r_view.png"]):
        shutil.copyfile(source_path, "demo_output/gt_rgb/" + target_path)
    os.makedirs("demo_output/nrff_rgb", exist_ok=True)
    for source_path, target_path in zip(nrff_rgb, ["l_view.png", "c_view.png", "r_view.png"]):
        shutil.copyfile(source_path, "demo_output/nrff_rgb/" + target_path)
    os.makedirs("demo_output/refnerf_rgb", exist_ok=True)
    for source_path, target_path in zip(refnerf_rgb, ["l_view.png", "c_view.png", "r_view.png"]):
        shutil.copyfile(source_path, "demo_output/refnerf_rgb/" + target_path)

    #WRITE NORMAL IMAGES
    os.makedirs("demo_output/refnerf_normals", exist_ok=True)
    for source_path, target_path in zip(refnerf_normals, ["l_view.png", "c_view.png", "r_view.png"]):
        shutil.copyfile(source_path, "demo_output/refnerf_normals/" + target_path)
    os.makedirs("demo_output/nrff_normals", exist_ok=True)
    for source_path, target_path in zip(nrff_normals, ["l_view.png", "c_view.png", "r_view.png"]):
        shutil.copyfile(source_path, "demo_output/nrff_normals/" + target_path)

find_demo_images("/home/Imatge/projects/AI4Heritage/albert/ipol/Albert_demo_mlbriefs4/models/gt/toaster/transforms_demo_ipol.json", "toaster", 10)