import argparse
from tissue_segmentation.core import process_slide

def main():
    parser = argparse.ArgumentParser(
        description="Segment tissue in a WSI, extract patch positions, and create overlay images."
    )
    parser.add_argument("--wsi_path", required=True, help="Path to input WSI (.tif/.svs file)")
    parser.add_argument("--onnx_model", required=True, help="Path to ONNX model file")
    parser.add_argument("--output_dir", required=True, help="Directory to save outputs")
    parser.add_argument("--thumbnail_patch_size", type=int, default=9)
    parser.add_argument("--scale_factor", type=float, default=0.01)
    parser.add_argument("--tissue_threshold", type=float, default=0.6)
    parser.add_argument("--model_input_size", type=int, default=500)
    parser.add_argument("--mask_threshold", type=float, default=0.6)
    args = parser.parse_args()

    process_slide(
        wsi_path=args.wsi_path,
        onnx_model=args.onnx_model,
        output_dir=args.output_dir,
        thumbnail_patch_size=args.thumbnail_patch_size,
        scale_factor=args.scale_factor,
        tissue_threshold=args.tissue_threshold,
        model_input_size=args.model_input_size,
        mask_threshold=args.mask_threshold
    )

if __name__ == "__main__":
    main()
