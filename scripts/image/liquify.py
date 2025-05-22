import torch
import torch.nn.functional as F
import numpy as np


class ImageLiquify:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "image": ("IMAGE",),
            "x_coord": ("INT", {"default": 0, "min": -8192, "max": 8192, "step": 1}),
            "y_coord": ("INT", {"default": 0, "min": -8192, "max": 8192, "step": 1}),
            "strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 10.0, "step": 0.01}),
            "effect_type": (["push", "expand", "shrink", "twirl"], {"default": "push"}),
        },
        "optional": {
            "mask": ("MASK",),
            "shape_type": (["circle", "oval", "rectangle"], {"default": "circle"}),
            "radius_major": ("INT", {"default": 100, "min": 1, "max": 2048, "step": 1}),
            "radius_minor": ("INT", {"default": 100, "min": 1, "max": 2048, "step": 1}),
            "push_direction_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
            "push_direction_y": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
        }
    }

  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "main"
  CATEGORY = "ComfyUI-Extended/Image"

  def main(self, image: torch.Tensor, x_coord: int, y_coord: int, strength: float, effect_type: str,
           mask: torch.Tensor = None,
           shape_type: str = "circle", radius_major: int = 100, radius_minor: int = 100,
           push_direction_x: float = 0.0, push_direction_y: float = 0.0):

    if image.ndim == 3:  # HWC
      image = image.unsqueeze(0)  # BHWC

    batch_size, height, width, channels = image.shape
    device = image.device

    img_to_process = image[0]  # Process first image in batch (H, W, C)

    yy, xx = torch.meshgrid(torch.arange(height, device=device, dtype=torch.float32),
                            torch.arange(width, device=device,
                                         dtype=torch.float32),
                            indexing='ij')

    effective_center_x = torch.tensor(
        float(x_coord), device=device, dtype=torch.float32)
    effective_center_y = torch.tensor(
        float(y_coord), device=device, dtype=torch.float32)
    use_mask_mode = False
    single_mask_tensor = None

    if mask is not None and mask.nelement() > 0:
      if mask.ndim == 3 and mask.shape[0] == batch_size:  # B, H, W
        candidate_mask = mask[0].to(device=device, dtype=torch.float32)
      # B, 1, H, W
      elif mask.ndim == 4 and mask.shape[0] == batch_size and mask.shape[1] == 1:
        candidate_mask = mask[0, 0].to(device=device, dtype=torch.float32)
      # H, W (assuming from a node that outputs a single mask)
      elif mask.ndim == 2:
        candidate_mask = mask.to(device=device, dtype=torch.float32)
      else:
        print(
            f"Warning: Mask tensor has unexpected shape {mask.shape}. Ignoring mask.")
        candidate_mask = None

      if candidate_mask is not None:
        if candidate_mask.shape[0] == height and candidate_mask.shape[1] == width:
          single_mask_tensor = candidate_mask
          use_mask_mode = True
          active_mask_points = torch.where(single_mask_tensor > 0.1)
          if active_mask_points[0].numel() > 0 and active_mask_points[1].numel() > 0:
            effective_center_y = torch.mean(active_mask_points[0].float())
            effective_center_x = torch.mean(active_mask_points[1].float())
          else:
            print(f"Warning: Mask provided but no significant area above threshold 0.1 found for centroid. Using input/default center coordinates.")
        else:
          print(
              f"Warning: Liquify mask size ({candidate_mask.shape[1]}x{candidate_mask.shape[0]}) does not match image size ({width}x{height}). Ignoring mask.")
          use_mask_mode = False  # Fallback

    dx_map = xx - effective_center_x
    dy_map = yy - effective_center_y

    is_inside_map = torch.zeros_like(xx, dtype=torch.bool, device=device)
    normalized_dist_map = torch.ones_like(
        xx, dtype=torch.float32, device=device)

    eff_radius_major_val = float(max(1, radius_major))
    eff_radius_minor_val = float(max(1, radius_minor))

    if use_mask_mode and single_mask_tensor is not None:
      is_inside_map = single_mask_tensor > 0.001
      normalized_dist_map = torch.where(
          is_inside_map, 1.0 - single_mask_tensor, normalized_dist_map)
    else:
      if shape_type == "circle":
        eff_radius_minor_val = eff_radius_major_val

      safe_radius_major = torch.clamp(torch.tensor(
          eff_radius_major_val, device=device), min=1e-6)
      safe_radius_minor = torch.clamp(torch.tensor(
          eff_radius_minor_val, device=device), min=1e-6)

      if shape_type == "circle":
        distance_squared = dx_map**2 + dy_map**2
        is_inside_map = distance_squared < safe_radius_major**2
        current_dist = torch.sqrt(distance_squared)
        normalized_dist_map = torch.where(
            is_inside_map, current_dist / safe_radius_major, normalized_dist_map)
      elif shape_type == "oval":
        val_in_ellipse_eq = (dx_map**2 / safe_radius_major **
                             2) + (dy_map**2 / safe_radius_minor**2)
        is_inside_map = val_in_ellipse_eq < 1.0
        normalized_dist_map = torch.where(
            is_inside_map, torch.sqrt(val_in_ellipse_eq), normalized_dist_map)
      elif shape_type == "rectangle":
        is_inside_map = (torch.abs(dx_map) < safe_radius_major) & (
            torch.abs(dy_map) < safe_radius_minor)
        norm_dx = torch.abs(dx_map) / safe_radius_major
        norm_dy = torch.abs(dy_map) / safe_radius_minor
        max_norm_dist = torch.maximum(norm_dx, norm_dy)
        normalized_dist_map = torch.where(
            is_inside_map, max_norm_dist, normalized_dist_map)

    normalized_dist_map = torch.clamp(normalized_dist_map, 0.0, 1.0)
    falloff_factor_map = 1.0 - normalized_dist_map
    falloff_factor_map = torch.where(
        is_inside_map, falloff_factor_map, torch.zeros_like(falloff_factor_map))

    src_x_map = xx.clone()
    src_y_map = yy.clone()

    if effect_type == "push":
      ref_dim_for_push = (eff_radius_major_val + eff_radius_minor_val) / \
          2.0 if not use_mask_mode else float(min(width, height)) * 0.1
      displacement_magnitude = strength * \
          falloff_factor_map * (ref_dim_for_push * 0.1)
      delta_x = push_direction_x * displacement_magnitude
      delta_y = push_direction_y * displacement_magnitude

      current_src_x = xx + delta_x
      current_src_y = yy + delta_y
      src_x_map = torch.where(is_inside_map, current_src_x, src_x_map)
      src_y_map = torch.where(is_inside_map, current_src_y, src_y_map)

    elif effect_type == "expand":
      shift_factor = strength * falloff_factor_map
      shift_factor = torch.clamp(shift_factor, max=0.999)
      new_distance_ratio = 1.0 - shift_factor

      current_src_x = effective_center_x + dx_map * new_distance_ratio
      current_src_y = effective_center_y + dy_map * new_distance_ratio
      src_x_map = torch.where(is_inside_map, current_src_x, src_x_map)
      src_y_map = torch.where(is_inside_map, current_src_y, src_y_map)

    elif effect_type == "shrink":
      factor = strength * falloff_factor_map
      new_distance_ratio = 1.0 + factor

      current_src_x = effective_center_x + dx_map * new_distance_ratio
      current_src_y = effective_center_y + dy_map * new_distance_ratio
      src_x_map = torch.where(is_inside_map, current_src_x, src_x_map)
      src_y_map = torch.where(is_inside_map, current_src_y, src_y_map)

    elif effect_type == "twirl":
      # Negative for clockwise in typical image coordinates
      angle_rad = strength * (falloff_factor_map**2)
      cos_angle = torch.cos(-angle_rad)
      sin_angle = torch.sin(-angle_rad)

      rotated_dx = dx_map * cos_angle - dy_map * sin_angle
      rotated_dy = dx_map * sin_angle + dy_map * cos_angle

      current_src_x = effective_center_x + rotated_dx
      current_src_y = effective_center_y + rotated_dy
      src_x_map = torch.where(is_inside_map, current_src_x, src_x_map)
      src_y_map = torch.where(is_inside_map, current_src_y, src_y_map)

    img_for_grid_sample = img_to_process.permute(
        2, 0, 1).unsqueeze(0)  # (1, C, H, W)

    normalized_src_x_map = (src_x_map / (width - 1.0)) * 2.0 - 1.0
    normalized_src_y_map = (src_y_map / (height - 1.0)) * 2.0 - 1.0

    grid = torch.stack((normalized_src_x_map, normalized_src_y_map),
                       dim=-1).unsqueeze(0)  # (1, H, W, 2)

    output_sampled = F.grid_sample(img_for_grid_sample, grid,
                                   mode='bilinear', padding_mode='border',
                                   align_corners=True)

    final_output_tensor = output_sampled.permute(0, 2, 3, 1)  # (1, H, W, C)

    return (final_output_tensor,)
