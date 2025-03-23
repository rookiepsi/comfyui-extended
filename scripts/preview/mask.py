import folder_paths
import random
from nodes import SaveImage


class PreviewMask(SaveImage):
  def __init__(self):
    self.output_dir = folder_paths.get_temp_directory()
    self.type = "temp"
    self.prefix_append = f"_temp_{''.join(random.choices('abcdefghijklmnopqrstupvxyz', k=5))}"
    self.compress_level = 4

  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "mask": ("MASK", {}),
        },
    }

  RETURN_TYPES = ()
  CATEGORY = "comfyui-extended/preview"
  FUNCTION = "main"
  OUTPUT_NODE = True

  def main(self, mask):
    reshaped_mask = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1]))
    preview = reshaped_mask.movedim(1, -1).expand(-1, -1, -1, 3)
    return self.save_images(preview)
