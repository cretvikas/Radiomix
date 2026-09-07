"""
Co-registration feature module.
Extracted from CoRegistration(1).ipynb — code preserved exactly as in the notebook.
"""
import SimpleITK as sitk


def coregister_images(fixed_path, moving_path, output_path):
    print(f"\n--- Registering {moving_path} → {fixed_path} ---")

    fixed = sitk.ReadImage(fixed_path, sitk.sitkFloat32)
    moving = sitk.ReadImage(moving_path, sitk.sitkFloat32)

    # 1. Initial alignment (VERY IMPORTANT)
    initial_transform = sitk.CenteredTransformInitializer(
        fixed,
        moving,
        sitk.Euler3DTransform(),
        sitk.CenteredTransformInitializerFilter.GEOMETRY
    )

    # 2. Registration setup
    registration = sitk.ImageRegistrationMethod()

    # Metric (best for multi-modal MRI)
    registration.SetMetricAsMattesMutualInformation(50)

    # Speed optimization
    registration.SetMetricSamplingStrategy(registration.RANDOM)
    registration.SetMetricSamplingPercentage(0.01)

    # Interpolation
    registration.SetInterpolator(sitk.sitkLinear)

    # Optimizer
    registration.SetOptimizerAsGradientDescent(
        learningRate=1.0,
        numberOfIterations=100,
        convergenceMinimumValue=1e-6,
        convergenceWindowSize=10
    )

    registration.SetOptimizerScalesFromPhysicalShift()

    # Apply initial transform
    registration.SetInitialTransform(initial_transform, inPlace=False)

    # 3. Run registration
    final_transform = registration.Execute(fixed, moving)

    print("Final metric:", registration.GetMetricValue())
    print("Stop condition:", registration.GetOptimizerStopConditionDescription())

    # 4. Apply transform (CRUCIAL)
    registered = sitk.Resample(
        moving,
        fixed,
        final_transform,
        sitk.sitkLinear,
        0.0,
        moving.GetPixelID()
    )

    sitk.WriteImage(registered, output_path)

    return fixed, moving, registered
