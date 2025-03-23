class PrimitiveInteger:
  cache = 0

  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "value": ("INT", {"default": 0, "min": -1000000000000000, "max": 1000000000000000, "step": 1}),
            "step": ("INT", {"default": 1, "min": -1000000000000000, "max": 1000000000000000, "step": 1}),
            "min": ("INT", {"default": 0, "min": -1000000000000000, "max": 1000000000000000, "step": 1}),
            "max": ("INT", {"default": 1000000000000000, "min": -1000000000000000, "max": 1000000000000000, "step": 1}),
            "method": (["fixed", "increment", "decrement", "randomize", "previous"], {"default": "fixed"}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ("INT",)
  CATEGORY = "comfyui-extended/primitive"
  FUNCTION = "main"

  @classmethod
  def IS_CHANGED(cls, method, **kwargs):
    if method == "randomize":
      return int("NaN")

  def main(self, value, step, min, max, method, id):
    from server import PromptServer

    if method == "previous":
      value = self.cache
    else:
      self.cache = value

    PromptServer.instance.send_sync("comfyui-extended_primitive", {
        "id": id, "value": value, "step": step, "range": {"min": min, "max": max}, "method": method, "type": "integer"
    })

    return (value, {})
