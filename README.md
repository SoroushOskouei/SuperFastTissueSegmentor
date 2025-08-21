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

## Batch Processing: Process All Slides in a Folder

You can easily process all slides in a folder (e.g., `WSIs/`) using a simple shell loop.
Here’s an example command (for bash) that will run the CLI over every `.svs` and `.tif` file in the `WSIs` directory:

    for slide in WSIs/*.{svs,tif}; do
        python -m tissue_segmentation.cli \
            --wsi_path "$slide" \
            --onnx_model path/to/model.onnx \
            --output_dir ./results
    done

- All results will be saved in the `./results` directory.
- You can adjust the wildcard (`*.svs`, `*.tif`) for your file types.

**Tip:**
If you have only one file type (e.g., only `.svs`), you can simplify:

    for slide in WSIs/*.svs; do
        python -m tissue_segmentation.cli \
            --wsi_path "$slide" \
            --onnx_model path/to/model.onnx \
            --output_dir ./results
    done


## Acknowledgment
The trained model is in part based upon open-access data from TCGA Research Network: https://www.cancer.gov/tcga.
