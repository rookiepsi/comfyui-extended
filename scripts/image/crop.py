import torch
import torch.nn.functional as F


class rookiepsi_CropImageToMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "padding": (
                    "INT",
                    {"default": 0, "min": -8192, "max": 8192, "step": 1},
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "main"
    CATEGORY = "comfyUI-extended/image"

    def main(self, image: torch.Tensor, mask: torch.Tensor, padding: int):
        cropped_images = []

        for img, msk in zip(image, mask):
            h, w, _ = img.shape

            if msk.sum() == 0:
                cropped_images.append(img)
                continue

            rows = torch.any(msk, axis=1)
            cols = torch.any(msk, axis=0)
            y_indices, x_indices = torch.where(rows)[0], torch.where(cols)[0]

            if y_indices.numel() == 0 or x_indices.numel() == 0:
                cropped_images.append(img)
                continue

            y_start = max(0, y_indices.min().item() - padding)
            y_end = min(h, y_indices.max().item() + 1 + padding)
            x_start = max(0, x_indices.min().item() - padding)
            x_end = min(w, x_indices.max().item() + 1 + padding)

            cropped_image = img[y_start:y_end, x_start:x_end, :]
            cropped_images.append(cropped_image)

        if not cropped_images:
            return (image,)

        max_h = max(img.shape[0] for img in cropped_images)
        max_w = max(img.shape[1] for img in cropped_images)

        padded_images = []
        for img in cropped_images:
            h_diff = max_h - img.shape[0]
            w_diff = max_w - img.shape[1]

            pad_top = h_diff // 2
            pad_bottom = h_diff - pad_top
            pad_left = w_diff // 2
            pad_right = w_diff - pad_left

            padding_dims = (0, 0, pad_left, pad_right, pad_top, pad_bottom)

            padded_img = F.pad(img, padding_dims, "constant", 0)
            padded_images.append(padded_img)

        output_tensor = torch.stack(padded_images)

        return (output_tensor,)
