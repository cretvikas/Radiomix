"""
N4 Bias Field Correction feature module.
Extracted from N4BiasCorrection(1).ipynb — code preserved exactly as in the notebook.
"""
import SimpleITK as sitk
import os


def bias_correct_nifti(input_path, output_path):
    print(f"--- 💡 N4 Bias Correction: {input_path} ---")

    # 1. Read Image
    # sitk.ReadImage returns a SimpleITK object (not numpy array)
    image = sitk.ReadImage(input_path)

    # 2. Convert to Float32
    # N4 requires float data. We cast it to ensure compatibility.
    image = sitk.Cast(image, sitk.sitkFloat32)

    # 3. Create a Mask (Crucial Step!)
    # The bias field exists everywhere, but we only care about the brain.
    # Calculating bias in the empty black air throws off the algorithm.
    # We create a simple mask: Any pixel > 0 is "tissue".
    print("   Creating mask...")
    mask_image = sitk.OtsuThreshold(image, 0, 1, 200)

    # 4. Set up the N4 Corrector
    print("   Running N4 Bias Field Correction (this may take a moment)...")
    corrector = sitk.N4BiasFieldCorrectionImageFilter()

    # Optional: Tweaking parameters for performance vs accuracy
    # max_iterations: [50, 50, 50, 50] is standard.
    # It runs at different resolutions (multi-scale) to catch both large and small shadows.
    corrector.SetMaximumNumberOfIterations([50, 50, 50, 50])

    # 5. Execute
    # The input is the image AND the mask.
    # The output is the corrected image.
    corrected_image = corrector.Execute(image, mask_image)

    # 6. Save
    sitk.WriteImage(corrected_image, output_path)
    print(f"✅ Saved corrected file to: {output_path}")

    # 7. (Optional) Re-read to return for visualization
    return image, corrected_image
