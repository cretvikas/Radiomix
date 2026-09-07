# Radiomics MRI Analysis Web Application

An end-to-end pipeline for preprocessing brain MRI scans (DICOM/NIfTI) and extracting radiomics features for automated tumor region analysis.

## Tech Stack
- **Core:** Python, SimpleITK, NiBabel, scikit-image, pydicom
- **Radiomics/ML:** PyRadiomics, Scikit-learn
- **App:** Flask / React
- **Formats:** DICOM, NIfTI
- **Performance:** Multithreading for non-blocking UI during scan processing

## Features / Preprocessing Pipeline

| Module | Status | Description |
|---|---|---|
| `visualization.py` | ✅ Implemented | DICOM series loading, slice sorting, 3D volume stacking, affine construction, and display normalization for DICOM → NIfTI conversion. |
| `denoising.py` | ✅ Implemented | Non-Local Means denoising on NIfTI volumes with Rician noise sigma estimation (`skimage.restoration`). |
| `n4_bias_correction.py` | ✅ Implemented | N4 Bias Field Correction using SimpleITK with Otsu-based tissue masking. |
| `coregistration.py` | ✅ Implemented | Multi-modal rigid registration (Euler3D) using Mattes Mutual Information and gradient descent optimization (SimpleITK). |
| `normalization.py` | 🚧 In Progress | Intensity normalization (z-score / min-max / percentile) — interface defined, implementation pending. |
| `skull_stripping.py` | 🚧 In Progress | Brain extraction (Otsu / BET-style / deep learning) — interface defined, implementation pending. |

Each module exposes a simple `input_path → output_path` function so it can be called independently or chained into a full pipeline.

## Project Structure
```
features/
├── __init__.py
├── coregistration.py
├── denoising.py
├── n4_bias_correction.py
├── normalization.py
├── skull_stripping.py
└── visualization.py
```

## Roadmap
- [ ] Implement `normalization.py`
- [ ] Implement `skull_stripping.py`
- [ ] Wire preprocessing modules into a Flask/React pipeline UI
- [ ] Add PyRadiomics feature extraction
- [ ] Train/evaluate ML model for tumor region identification (accuracy/AUC benchmarking)
- [ ] Add multithreaded task queue for responsive UI during processing

## Requirements
```
SimpleITK
nibabel
numpy
pydicom
scikit-image
```

## Usage Example
```python
from features.n4_bias_correction import bias_correct_nifti
from features.denoising import denoise_nifti
from features.coregistration import coregister_images

bias_correct_nifti("input.nii.gz", "bias_corrected.nii.gz")
denoise_nifti("bias_corrected.nii.gz", "denoised.nii.gz")
coregister_images("fixed.nii.gz", "denoised.nii.gz", "registered.nii.gz")
```

## License
Add your preferred license here (e.g. MIT).
