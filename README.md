# SuperFastTissueSegmentor

This tool segments tissue regions from Whole Slide Images (WSIs) using an ONNX model, extracts patch positions, and creates an overlay thumbnail for visualization.

## Installation

First, install dependencies (preferably in a fresh Python environment):

    pip install -r requirements.txt

## Usage

Run the CLI module on a single slide:

    python -m tissue_segmentation.cli \
        --wsi_path example_slide.svs \
        --onnx_model path/to/model.onnx \
        --output_dir ./results

**Outputs:**
- <slide>_patches.json: Patch positions and parameters.
- <slide>_overlay.png: Thumbnail with patches visualized.

## CLI Arguments

- --wsi_path: Path to the input WSI (e.g., `.svs` or `.tif` file)
- --onnx_model: Path to the tissue segmentation ONNX model
- --output_dir: Output directory for results
- --thumbnail_patch_size: Patch size (in thumbnail pixels, default=9)
- --scale_factor: Resize factor for thumbnail (default=0.01)
- --tissue_threshold: Tissue percentage required per patch (default=0.6)
- --model_input_size: Input size for ONNX model (default=500)
- --mask_threshold: Threshold for binarizing tissue mask (default=0.6)

To see all options:

    python -m tissue_segmentation.cli --help

## Example Output

You will find a JSON file with patch positions, and a PNG image overlaying detected patches on the slide thumbnail.
