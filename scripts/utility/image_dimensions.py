class UtilityImageDimensions:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "image": ("IMAGE", {}),
        },
    }

  RETURN_TYPES = ("INT", "INT")
  RETURN_NAMES = ("width", "height")
  CATEGORY = "comfyui-extended/utility"
  FUNCTION = "main"

  def main(self, image):
    return (int(image.shape[2]), int(image.shape[1]))
