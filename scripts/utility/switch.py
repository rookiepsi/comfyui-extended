class AnyType(str):
  def __ne__(self, __value: object) -> bool:
    return False

  def __call__(self, *args, **kwargs):
    return self


any = AnyType("*")


class UtilitySwitch:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "true": (any, {}),
            "false": (any, {}),
            "condition": ("BOOLEAN", {"default": False}),
        }
    }

  RETURN_TYPES = ("*",)
  RETURN_NAMES = ("output",)
  FUNCTION = "main"
  CATEGORY = "comfyui-extended/utility"

  def main(self, true, false, condition):
    return (true if condition else false, {})
