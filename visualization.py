"""
Visualization / DICOM loading feature module.
Extracted from visualization(1).ipynb and main.py helper functions.
"""
import os
import numpy as np
import pydicom
import nibabel as nib


def load_dicom_series(folder_path):
    """Scan a folder and return paths of valid DICOM files.

    A file is considered valid if it can be parsed by pydicom and contains
    both ImagePositionPatient and ImageOrientationPatient attributes.
    """
    dicom_files = []
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            ds = pydicom.dcmread(fpath, stop_before_pixels=True)
        except Exception:
            continue
        if hasattr(ds, "ImagePositionPatient") and hasattr(ds, "ImageOrientationPatient"):
            dicom_files.append(fpath)
    if not dicom_files:
        raise ValueError("No valid DICOM files found in the selected folder.")
    return dicom_files


def load_slices(dicom_paths):
    """Read DICOM files, filter those with PixelData, and return sorted datasets."""
    dicoms = []
    for p in dicom_paths:
        try:
            ds = pydicom.dcmread(p)
            if hasattr(ds, "PixelData"):
                dicoms.append(ds)
        except Exception:
            continue
    dicoms.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    return dicoms


def stack_slices(dicoms):
    """Stack sorted DICOM datasets into a 3-D numpy volume (X, Y, Z)."""
    slices = [ds.pixel_array for ds in dicoms]
    volume = np.stack(slices)
    # Transpose from (Z, Y, X) → (X, Y, Z)
    return np.transpose(volume, (1, 2, 0)).astype(np.float32)


def build_affine(dicoms):
    """Build a NIfTI-compatible 4×4 affine matrix from DICOM metadata."""
    ref = dicoms[0]
    try:
        orientation = np.array(ref.ImageOrientationPatient).reshape(2, 3)
        row, col = orientation
        slice_dir = np.cross(row, col)
        pixel_spacing = np.array(ref.PixelSpacing)
        pos1 = np.array(dicoms[0].ImagePositionPatient)
        pos2 = np.array(dicoms[1].ImagePositionPatient)
        spacing = np.linalg.norm(pos2 - pos1)
        affine = np.eye(4)
        affine[:3, 0] = row * pixel_spacing[0]
        affine[:3, 1] = col * pixel_spacing[1]
        affine[:3, 2] = slice_dir * spacing
        affine[:3, 3] = pos1
    except Exception:
        affine = np.eye(4)
    return affine


def normalize_display(img):
    """Normalize a 2-D slice to uint8 [0, 255] for display."""
    img = img.astype(np.float32)
    lo, hi = img.min(), img.max()
    if hi == lo:
        return np.zeros_like(img, dtype=np.uint8)
    img = (img - lo) / (hi - lo)
    return (img * 255).astype(np.uint8)
