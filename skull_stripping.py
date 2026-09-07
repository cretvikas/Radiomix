"""
Skull Stripping feature module.
TODO: Implement skull stripping functions (Otsu-based, BET-style, deep learning, etc.)
"""


def skull_strip_nifti(input_path, output_path, method="otsu"):
    """Placeholder for future skull stripping implementation.

    Parameters
    ----------
    input_path : str
        Path to the input NIfTI file.
    output_path : str
        Path to save the skull-stripped NIfTI file.
    method : str
        Skull stripping method to use (e.g. 'otsu', 'bet').
    """
    raise NotImplementedError(
        "Skull stripping module is not yet implemented. "
        "Use the in-memory skull stripping in PreprocessingWorker for now."
    )
