class PreviewBoolean:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "boolean": ("BOOLEAN", {"forceInput": True}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ()
  CATEGORY = "comfyui-extended/preview"
  FUNCTION = "main"
  OUTPUT_NODE = True

  def main(self, boolean, id):
    from server import PromptServer

    if boolean is None:
      boolean = True

    PromptServer.instance.send_sync("comfyui-extended_preview", {
        "id": id,
        "value": str(boolean).lower()
    })

    return ()
