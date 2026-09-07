"""
Normalization feature module.
TODO: Implement intensity normalization functions (z-score, min-max, histogram matching, etc.)
"""


def normalize_nifti(input_path, output_path, method="zscore"):
    """Placeholder for future normalization implementation.

    Parameters
    ----------
    input_path : str
        Path to the input NIfTI file.
    output_path : str
        Path to save the normalized NIfTI file.
    method : str
        Normalization method to use (e.g. 'zscore', 'minmax', 'percentile').
    """
    raise NotImplementedError(
        "Normalization module is not yet implemented. "
        "Use the in-memory normalization in PreprocessingWorker for now."
    )
