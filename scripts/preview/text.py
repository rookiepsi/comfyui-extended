class PreviewText:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "text": ("STRING", {"forceInput": True}),
        },
        "hidden": {
            "id": "UNIQUE_ID"
        }
    }

  RETURN_TYPES = ()
  CATEGORY = "comfyui-extended/preview"
  FUNCTION = "main"
  OUTPUT_NODE = True

  def main(self, text, id):
    from server import PromptServer

    if text is None:
      text = ""

    PromptServer.instance.send_sync("comfyui-extended_preview", {
        "id": id,
        "value": text
    })

    return ()
