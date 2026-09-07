"""
Denoising feature module.
Extracted from Denoising(1).ipynb — code preserved exactly as in the notebook.
"""
import nibabel as nib
import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma


def denoise_nifti(input_path, output_path):
    print(f"--- 🧹 Denoising: {input_path} ---")

    # 1. Load NIfTI
    nii = nib.load(input_path)
    data = nii.get_fdata()

    # 2. Estimate the Noise Standard Deviation
    # MRI noise is "Rician," which varies across the image.
    # We estimate sigma (noise level) from the background.
    sigma_est = np.mean(estimate_sigma(data, channel_axis=None))
    print(f"   Estimated Noise Sigma: {sigma_est:.4f}")

    # 3. Apply Non-Local Means Denoising
    # patch_size: size of the area to compare (5x5x5 is standard)
    # patch_distance: how far to look for similar patches (6 is standard)
    # h: cut-off distance (higher = smoother but more blur). 1.15 * sigma is a good starting point.

    print("   Applying Non-Local Means (this may take a moment for 3D)...")
    denoised_data = denoise_nl_means(
        data,
        h=1.15 * sigma_est,
        fast_mode=True,
        patch_size=5,
        patch_distance=6,
        channel_axis=None  # Treat as 3D volume, not 2D slices
    )

    # 4. Save Result
    # specific step: Copy the header/affine from the original so alignment doesn't break!
    new_nii = nib.Nifti1Image(denoised_data, nii.affine, nii.header)
    nib.save(new_nii, output_path)
    print(f"✅ Saved denoised file to: {output_path}")
