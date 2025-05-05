class ImageSwitch:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "switch": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
        },
        "optional": {
            "i1": ("IMAGE", {}),
            "i2": ("IMAGE", {}),
            "i3": ("IMAGE", {}),
            "i4": ("IMAGE", {}),
        }
    }

  def __init__(self):
    pass

  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "main"
  CATEGORY = "comfyui-extended/switch"

  def main(self, switch, i1=None, i2=None, i3=None, i4=None):
    output = i1

    if (switch == 2):
      output = i2
    elif (switch == 3):
      output = i3
    elif (switch == 4):
      output = i4

    return (output, {})
