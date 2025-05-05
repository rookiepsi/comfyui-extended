class ImageSwitch:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "switch": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
        },
        "optional": {
            "image_1": ("IMAGE", {}),
            "image_2": ("IMAGE", {}),
            "image_3": ("IMAGE", {}),
            "image_4": ("IMAGE", {}),
        }
    }

  def __init__(self):
    pass

  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "main"
  CATEGORY = "comfyui-extended/switch"

  def main(self, switch, image_1=None, image_2=None, image_3=None, image_4=None):
    if (switch == 1):
      return (image_1, {})

    if (switch == 2):
      return (image_2, {})

    if (switch == 3):
      return (image_3, {})

    if (switch == 4):
      return (image_4, {})
