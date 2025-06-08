import math
import numpy as np
import torch

from PIL import Image, ImageDraw, ImageFilter


class rookiepsi_ConstructMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 1, "max": 8192, "step": 1}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192, "step": 1}),
                "shape": (
                    ["rectangle", "ellipse", "triangle"],
                    {"default": "rectangle"},
                ),
                "shape_width": (
                    "INT",
                    {"default": 256, "min": 1, "max": 8192, "step": 1},
                ),
                "shape_height": (
                    "INT",
                    {"default": 256, "min": 1, "max": 8192, "step": 1},
                ),
                "x": ("INT", {"default": 256, "min": -8192, "max": 8192, "step": 1}),
                "y": ("INT", {"default": 256, "min": -8192, "max": 8192, "step": 1}),
                "angle": (
                    "FLOAT",
                    {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1},
                ),
                "border_radius": (
                    "INT",
                    {"default": 0, "min": 0, "max": 2048, "step": 1},
                ),
                "blur": ("INT", {"default": 0, "min": 0, "max": 2048, "step": 1}),
                "strength": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "antialiasing": ("INT", {"default": 2, "min": 1, "max": 4, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "main"
    CATEGORY = "ComfyUI-Extended/Mask"

    def main(
        self,
        width: int,
        height: int,
        shape: str,
        shape_width: int,
        shape_height: int,
        x: int,
        y: int,
        angle: float = 0.0,
        border_radius: int = 0,
        blur: int = 0,
        strength: float = 1.0,
        antialiasing: int = 2,
    ):
        if strength == 0.0:
            return (torch.zeros((1, height, width), dtype=torch.float32),)

        ss_factor = max(1, antialiasing)

        if angle != 0.0:
            rad = math.radians(abs(angle))
            cos_r, sin_r = math.cos(rad), math.sin(rad)
            rotated_w = abs(shape_width * cos_r) + abs(shape_height * sin_r)
            rotated_h = abs(shape_width * sin_r) + abs(shape_height * cos_r)
            final_canvas_size = int(max(rotated_w, rotated_h) + (border_radius * 2))
        else:
            final_canvas_size = max(shape_width, shape_height) + (border_radius * 2)

        final_canvas_size += 4

        ss_canvas_size = final_canvas_size * ss_factor
        shape_img = Image.new("L", (ss_canvas_size, ss_canvas_size), 0)
        draw = ImageDraw.Draw(shape_img)

        cx = ss_canvas_size // 2
        cy = ss_canvas_size // 2

        padded_sw = shape_width * ss_factor
        padded_sh = shape_height * ss_factor

        left = cx - padded_sw // 2
        top = cy - padded_sh // 2
        right = cx + padded_sw // 2
        bottom = cy + padded_sh // 2

        ss_border_radius = border_radius * ss_factor

        if shape == "ellipse":
            draw.ellipse([left, top, right, bottom], fill=255)
        elif shape == "rectangle":
            if ss_border_radius > 0:
                max_radius = min((right - left) // 2, (bottom - top) // 2)
                radius = min(ss_border_radius, max_radius)
                draw.rounded_rectangle(
                    [left, top, right, bottom], radius=radius, fill=255
                )
            else:
                draw.rectangle([left, top, right, bottom], fill=255)
        elif shape == "triangle":
            points = [(cx, top), (left, bottom), (right, bottom)]
            draw.polygon(points, fill=255)

            if ss_border_radius > 0:
                shape_img = shape_img.filter(
                    ImageFilter.GaussianBlur(radius=ss_border_radius)
                )
                shape_img = shape_img.point(lambda p: 255 if p > 128 else 0, "L")

        if ss_factor > 1:
            shape_img = shape_img.resize(
                (final_canvas_size, final_canvas_size),
                resample=Image.Resampling.LANCZOS,
            )

        if angle != 0.0:
            shape_img = shape_img.rotate(
                -angle, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=0
            )

        shape_np = np.array(shape_img, dtype=np.float32) / 255.0
        mask_np = np.zeros((height, width), dtype=np.float32)

        paste_x = x - shape_np.shape[1] // 2
        paste_y = y - shape_np.shape[0] // 2

        src_y_start = max(0, -paste_y)
        src_x_start = max(0, -paste_x)
        dst_y_start = max(0, paste_y)
        dst_x_start = max(0, paste_x)

        src_y_end = shape_np.shape[0] - max(0, (paste_y + shape_np.shape[0]) - height)
        src_x_end = shape_np.shape[1] - max(0, (paste_x + shape_np.shape[1]) - width)
        dst_y_end = min(height, paste_y + shape_np.shape[0])
        dst_x_end = min(width, paste_x + shape_np.shape[1])

        if (
            src_y_end > src_y_start
            and src_x_end > src_x_start
            and dst_y_end > dst_y_start
            and dst_x_end > dst_x_start
        ):
            mask_np[dst_y_start:dst_y_end, dst_x_start:dst_x_end] = shape_np[
                src_y_start:src_y_end, src_x_start:src_x_end
            ]

        if blur > 0:
            mask_pil = Image.fromarray((mask_np * 255).astype(np.uint8), "L")
            mask_pil = mask_pil.filter(ImageFilter.GaussianBlur(blur))
            mask_np = np.array(mask_pil, dtype=np.float32) / 255.0

        if strength != 1.0:
            mask_np *= strength

        return (torch.from_numpy(mask_np).unsqueeze(0),)
