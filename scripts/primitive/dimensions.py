class PrimitiveDimensions:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "list": ("STRING", {"default": "", "multiline": True,  "placeholder": "Comma separated list of dimensions: 832x1216, 1216x832, 1024x1024"}),
        }
    }

  RETURN_TYPES = ("INT", "INT")
  RETURN_NAMES = ("width", "height")
  CATEGORY = "comfyui-extended/primitive"
  FUNCTION = "main"

  @classmethod
  def VALIDATE_INPUTS(cls, list):
    import re

    if not re.match(r"^\d+x\d+(\s*,\s*\d+x\d+)*$", list):
      return "Primitive Dimensions: The input must be a comma separated list of {width}x{height}."
    else:
      return True

  @classmethod
  def IS_CHANGED(cls, list, **kwargs):
    pairs = list.split(",")

    if len(pairs) > 1:
      return int("NaN")

  def main(self, list):
    import random

    array = []
    pairs = list.split(",")

    for pair in pairs:
      w, h = pair.strip().split("x")
      array.append((int(w), int(h)))

    selected = random.choice(array)

    return selected
