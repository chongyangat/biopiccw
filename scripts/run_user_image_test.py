"""Run a direct read test for a user-provided 3-channel JPG using skimage."""

from __future__ import annotations

import argparse
from pathlib import Path

from skimage import io

from biopiccw.pipeline import render_pipeline, save_image

DEFAULT_IMAGE = r"D:\vrcontent\biopiccw\test.jpg"


def main() -> None:
    parser = argparse.ArgumentParser(description="Read and test user image with skimage")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="Input image path")
    parser.add_argument("--output", default="user_test_output.jpg", help="Output path")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = io.imread(str(image_path))
    if img is None:
        raise RuntimeError(f"skimage.io.imread failed for {image_path}")

    print("skimage read success, shape:", getattr(img, "shape", None))

    rendered = render_pipeline(
        image_path=image_path,
        magnification_factor=2.0,
        contrast_factor=1.5,
        sharpness_factor=2.0,
        gamma=2.2,
        delay_seconds=0.0,
    )
    save_image(rendered, args.output)
    print("render success, output saved to:", args.output)


if __name__ == "__main__":
    main()
