class PreviewInteger:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "int": ("INT", {"forceInput": True}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ()
  CATEGORY = "comfyui-extended/preview"
  FUNCTION = "main"
  OUTPUT_NODE = True

  def main(self, int, id):
    from server import PromptServer

    if int is None:
      int = 0

    PromptServer.instance.send_sync("comfyui-extended_preview", {
        "id": id,
        "value": str(int)
    })

    return ()
