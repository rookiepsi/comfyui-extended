class MaskSwitch:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "switch": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
        },
        "optional": {
            "mask_1": ("MASK", {}),
            "mask_2": ("MASK", {}),
            "mask_3": ("MASK", {}),
            "mask_4": ("MASK", {}),
        }
    }

  def __init__(self):
    pass

  RETURN_TYPES = ("MASK",)
  FUNCTION = "main"
  CATEGORY = "comfyui-extended/switch"

  def main(self, switch, mask_1=None, mask_2=None, mask_3=None, mask_4=None):
    if (switch == 1):
      return (mask_1, {})

    if (switch == 2):
      return (mask_2, {})

    if (switch == 3):
      return (mask_3, {})

    if (switch == 4):
      return (mask_4, {})
