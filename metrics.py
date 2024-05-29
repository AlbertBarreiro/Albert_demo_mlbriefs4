import numpy as np
import sys
import imageio.v2 as imageio
from piqa.ssim import SSIM
from piqa.lpips import LPIPS
import torch
from torchvision import transforms as T
import skimage.transform as st


def resize(img_read, shape):
    """
    Resizes the input image to the specified shape using anti-aliasing.

    Parameters:
    img_read (numpy.ndarray): Input image to be resized.
    shape (tuple): Desired output shape as (height, width).

    Returns:
    numpy.ndarray: Resized image.
    """
    h, w = shape  # Desired height and width
    return st.resize(img_read, (w, h), anti_aliasing=True, preserve_range=True)

# Transform to convert a PIL image or numpy array to a PyTorch tensor
tensor_transform = T.ToTensor()

def img2mse(x, y):
    """
    Computes the Mean Squared Error (MSE) between two tensors.

    Parameters:
    x (torch.Tensor): First input tensor.
    y (torch.Tensor): Second input tensor.

    Returns:
    torch.Tensor: Computed MSE.
    """
    return torch.mean((x - y) ** 2)

def mse2psnr(mse):
    """
    Converts Mean Squared Error (MSE) to Peak Signal-to-Noise Ratio (PSNR).

    Parameters:
    mse (torch.Tensor): Input MSE.

    Returns:
    torch.Tensor: Computed PSNR.
    """
    return -10.0 * torch.log10(mse)

def ssim(pred, gt):
    """
    Computes the Structural Similarity Index (SSIM) between two images.

    Parameters:
    pred (torch.Tensor): Predicted image tensor.
    gt (torch.Tensor): Ground truth image tensor.

    Returns:
    torch.Tensor: SSIM value.
    """
    ssim_model = SSIM().to(device=pred.device)

    # Normalize and add a batch dimension
    pred = torch.clip(pred.unsqueeze(0).float(), 0, 1)
    gt = torch.clip(gt.unsqueeze(0).float(), 0, 1)
    
    return ssim_model(pred, gt)

def lpips(pred, gt):
    """
    Computes the Learned Perceptual Image Patch Similarity (LPIPS) between two images using the VGG network.

    Parameters:
    pred (torch.Tensor): Predicted image tensor.
    gt (torch.Tensor): Ground truth image tensor.

    Returns:
    torch.Tensor: LPIPS value.
    """
    lpips_model = LPIPS(network="vgg").to(device=pred.device) 
    
    # Normalize and add a batch dimension
    pred = torch.clip(pred.unsqueeze(0).float(), 0, 1)
    gt = torch.clip(gt.unsqueeze(0).float(), 0, 1)
    
    return lpips_model(pred, gt)

def save_float_value(file_path, value):
    """
    Saves a floating-point value to a specified file.

    Parameters:
    file_path (str): Path to the output file.
    value (float): Float value to be saved.

    """
    with open(file_path, 'w') as file:
        file.write(str(value))


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python image_display.py <image1_path> <image2_path> <output_path>")
        sys.exit(1)

    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    output_path = sys.argv[3]

    output_path_psnr =  output_path + "_psnr"
    output_path_ssim = output_path + "_ssim"
    output_path_lpips = output_path + "_lpips"

    image1 = imageio.imread(image1_path)
    image1 = (image1 / 255.0).astype(np.float32)

    image2 = imageio.imread(image2_path)
    image2 = tensor_transform(image2) 


    image1_resized = resize(image1, image2.shape[1:])

    if image1_resized.shape[2] == 4:
        alpha = image1_resized[..., -1:]
        image1_resized = image1_resized[..., :3] * alpha + (1.0 - alpha)

    image1_resized = tensor_transform(image1_resized) 

    #save_tensor_as_image(image1_resized, "./bbbbb.png")

    mse = img2mse(image1_resized, image2)
    save_float_value(output_path_psnr, mse2psnr(mse).item())
    
    save_float_value(output_path_ssim, ssim(image1_resized, image2).item())

    save_float_value(output_path_lpips, lpips(image1_resized, image2).item())
    

