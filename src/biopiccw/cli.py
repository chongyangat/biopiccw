"""Command line interface for biopiccw pipeline."""

from __future__ import annotations

import argparse

from .pipeline import render_pipeline, save_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render visual-aid simulation output image")
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--magnification", type=float, default=2.0)
    parser.add_argument("--contrast", type=float, default=1.5)
    parser.add_argument("--sharpness", type=float, default=2.0)
    parser.add_argument("--gamma", type=float, default=2.2)
    parser.add_argument("--delay", type=float, default=0.0, help="Latency simulation seconds")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    output_image = render_pipeline(
        image_path=args.input,
        magnification_factor=args.magnification,
        contrast_factor=args.contrast,
        sharpness_factor=args.sharpness,
        gamma=args.gamma,
        delay_seconds=args.delay,
    )
    save_image(output_image, args.output)
    print(f"Rendered image saved to {args.output}")


if __name__ == "__main__":
    main()
