class PrimitiveFloat:
  cache = 0.00

  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "value": ("FLOAT", {"default": 1.00, "min": -100, "max": 100, "step": 0.01}),
            "step": ("FLOAT", {"default": 0.05, "min": -100, "max": 100, "step": 0.01}),
            "min": ("FLOAT", {"default": 0.00, "min": -100, "max": 100, "step": 0.01}),
            "max": ("FLOAT", {"default": 1.00, "min": -100, "max": 100, "step": 0.01}),
            "method": (["fixed", "increment", "decrement", "randomize", "previous"], {"default": "fixed"}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ("FLOAT",)
  CATEGORY = "comfyui-extended/primitive"
  FUNCTION = "main"

  @classmethod
  def IS_CHANGED(cls, method, **kwargs):
    if method == "randomize":
      return float("NaN")

  def main(self, value, step, min, max, method, id):
    from server import PromptServer

    if method == "previous":
      value = self.cache
    else:
      self.cache = value

    PromptServer.instance.send_sync("comfyui-extended_primitive", {
        "id": id, "value": value, "step": step, "range": {"min": min, "max": max}, "method": method, "type": "float"
    })

    return (value, {})
