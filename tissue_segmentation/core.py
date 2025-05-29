import numpy as np
import onnxruntime as ort
from cucim import CuImage
import cv2
from pathlib import Path
from PIL import Image, ImageDraw
import json

def read_resized_thumbnail(wsi_path, scale_factor, max_thumbnail_level=7):
    """Return thumbnail (H×W×3 uint8) resized so that W,H ≈ level0_dim * scale_factor."""
    wsi = CuImage(str(wsi_path))
    lvl0_w, lvl0_h = wsi.resolutions["level_dimensions"][0]
    thumb_level = min(max_thumbnail_level, len(wsi.resolutions["level_dimensions"]) - 1)
    tl_w, tl_h = wsi.resolutions["level_dimensions"][thumb_level]
    thumb = wsi.read_region(location=(0, 0), size=(tl_w, tl_h), level=thumb_level)
    thumb = np.asarray(thumb)[..., :3] if thumb.shape[-1] == 4 else np.asarray(thumb)
    new_w, new_h = int(lvl0_w * scale_factor), int(lvl0_h * scale_factor)
    return cv2.resize(thumb, (new_w, new_h), interpolation=cv2.INTER_AREA)

def predict_mask_on_thumbnail(thumbnail, onnx_model, model_input_size=500, threshold=0.6):
    if not hasattr(predict_mask_on_thumbnail, "sess"):
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        predict_mask_on_thumbnail.sess = ort.InferenceSession(onnx_model, providers=providers)
    inp = cv2.resize(thumbnail, (model_input_size, model_input_size)).astype(np.float32) / 255.0
    inp = np.expand_dims(inp, 0)
    pred = predict_mask_on_thumbnail.sess.run(None, {"input": inp})[0][0, ..., 0]
    pred = cv2.resize(pred, (thumbnail.shape[1], thumbnail.shape[0]), interpolation=cv2.INTER_LINEAR)
    return (pred > threshold).astype(np.uint8)

def generate_patch_positions(binary_mask, thumbnail_patch_size, tissue_threshold, scale_factor):
    h, w = binary_mask.shape
    stride = thumbnail_patch_size
    half = thumbnail_patch_size // 2
    req_pixels = thumbnail_patch_size * thumbnail_patch_size * tissue_threshold
    thumb_positions = []
    for cy in range(half, h - half, stride):
        for cx in range(half, w - half, stride):
            window = binary_mask[cy - half : cy + half, cx - half : cx + half]
            if window.sum() >= req_pixels:
                thumb_positions.append((cx - half, cy - half))
    orig_positions = [(int(x / scale_factor), int(y / scale_factor)) for x, y in thumb_positions]
    orig_patch_size = thumbnail_patch_size / scale_factor
    return thumb_positions, orig_positions, orig_patch_size

def draw_overlay(thumbnail, thumb_positions, thumbnail_patch_size, out_path):
    im = Image.fromarray(thumbnail)
    draw = ImageDraw.Draw(im)
    for (x_tl, y_tl) in thumb_positions:
        rect = [x_tl, y_tl, x_tl + thumbnail_patch_size, y_tl + thumbnail_patch_size]
        draw.rectangle(rect, outline="yellow", width=1)
    im.save(out_path)

def process_slide(
    wsi_path,
    onnx_model,
    output_dir,
    thumbnail_patch_size=9,
    scale_factor=0.01,
    tissue_threshold=0.6,
    model_input_size=500,
    mask_threshold=0.6
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    slide_name = Path(wsi_path).stem

    # 1. Generate thumbnail
    thumb = read_resized_thumbnail(wsi_path, scale_factor)

    # 2. Predict mask
    mask = predict_mask_on_thumbnail(thumb, onnx_model, model_input_size, mask_threshold)

    # 3. Patch positions
    thumb_pos, orig_pos, orig_patch_size = generate_patch_positions(
        mask, thumbnail_patch_size, tissue_threshold, scale_factor
    )

    # 4. Overlay
    overlay_path = output_dir / f"{slide_name}_overlay.png"
    draw_overlay(thumb, thumb_pos, thumbnail_patch_size, overlay_path)

    # 5. Save JSON
    json_path = output_dir / f"{slide_name}_patches.json"
    out = {
        "thumbnail_patch_size": thumbnail_patch_size,
        "scale_factor": scale_factor,
        "orig_patch_size": orig_patch_size,
        "thumbnail_positions": thumb_pos,
        "original_positions": orig_pos,
    }
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Processed {wsi_path} - JSON and overlay saved to {output_dir}")
