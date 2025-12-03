import base64
import io
import math
from typing import Literal

from PIL import Image


def image_to_b64(image: Image.Image, format: Literal["jpeg", "png"] = "jpeg") -> str:
    image_bytes = io.BytesIO()
    if format == "png":
        image.save(image_bytes, format="PNG")
    elif format == "jpeg":
        image.save(image_bytes, format="JPEG", quality=90)
    else:
        raise ValueError(f"Invalid image format: {format}")
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
    return image_base64


# Copied from https://github.com/huggingface/transformers/blob/e15b06d8dc6fa132550311d63c9758b580f39bcc/src/transformers/models/qwen2_vl/image_processing_qwen2_vl.py#L55
def smart_resize(
    height: int, width: int, factor: int = 28, min_pixels: int = 56 * 56, max_pixels: int = 14 * 14 * 4 * 1280
):
    """Rescales the image so that the following conditions are met:

    1. Both dimensions (height and width) are divisible by 'factor'.

    2. The total number of pixels is within the range ['min_pixels', 'max_pixels'].

    3. The aspect ratio of the image is maintained as closely as possible.

    """
    if height < factor or width < factor:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(
            f"absolute aspect ratio must be smaller than 200, got {max(height, width) / min(height, width)}"
        )
    h_bar = round(height / factor) * factor
    w_bar = round(width / factor) * factor
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = math.floor(height / beta / factor) * factor
        w_bar = math.floor(width / beta / factor) * factor
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor
    return h_bar, w_bar
