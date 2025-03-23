class PrimitiveBoolean:
  cache = True

  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "value": ("BOOLEAN", {"default": True}),
            "method": (["fixed", "randomize", "previous"], {"default": "fixed"}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ("BOOLEAN",)
  CATEGORY = "comfyui-extended/primitive"
  FUNCTION = "main"

  @classmethod
  def IS_CHANGED(cls, method, **kwargs):
    if method == "randomize":
      return bool("NaN")

  def main(self, value, method, id):
    from server import PromptServer

    if method == "previous":
      value = self.cache
    else:
      self.cache = value

    PromptServer.instance.send_sync("comfyui-extended_primitive", {
        "id": id, "value": value, "method": method, "type": "boolean"
    })

    return (value, {})
