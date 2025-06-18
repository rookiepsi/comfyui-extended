import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image


class rookiepsi_ResizeMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "width": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 1}),
                "height": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 1}),
                "interpolation": (
                    ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"],
                    {"default": "nearest-exact"},
                ),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "main"
    CATEGORY = "comfyui-extended/mask"

    @staticmethod
    def lanczos(samples, width, height):
        images = [
            Image.fromarray(
                np.clip(255.0 * mask.squeeze(0).cpu().numpy(), 0, 255).astype(np.uint8)
            )
            for mask in samples
        ]
        images = [
            image.resize((width, height), resample=Image.Resampling.LANCZOS)
            for image in images
        ]
        images = [
            torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
            for image in images
        ]
        result = torch.stack(images)
        return result.to(samples.device, samples.dtype)

    def main(self, mask, width, height, interpolation):
        if width == 0 and height == 0:
            return (mask,)

        if width == 0 or height == 0:
            _, orig_h, orig_w = mask.shape
            aspect_ratio = orig_w / orig_h
            if width == 0:
                target_width = int(height * aspect_ratio)
                target_height = height
            else:
                target_width = width
                target_height = int(width / aspect_ratio)
        else:
            target_width, target_height = width, height

        target_h, target_w = max(1, target_height), max(1, target_width)

        if mask.shape[1] == target_h and mask.shape[2] == target_w:
            return (mask,)

        samples = mask.unsqueeze(1)

        if interpolation == "lanczos":
            resized_samples = self.lanczos(samples, target_w, target_h)
        else:
            resized_samples = F.interpolate(
                samples, size=(target_h, target_w), mode=interpolation
            )

        final_mask = resized_samples.squeeze(1)

        return (final_mask,)
