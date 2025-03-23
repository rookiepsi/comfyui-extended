class PreviewFloat:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "float": ("FLOAT", {"forceInput": True}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ()
  CATEGORY = "comfyui-extended/preview"
  FUNCTION = "main"
  OUTPUT_NODE = True

  def main(self, float, id):
    from server import PromptServer

    if float is None:
      float = 0.00

    PromptServer.instance.send_sync("comfyui-extended_preview", {
        "id": id,
        "value": str(round(float, 3))
    })

    return ()
