class PrimitiveText:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "text": ("STRING", {"default": "", "multiline": True, "placeholder": "text"}),
        }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("text",)
  CATEGORY = "comfyui-extended/primitive"
  FUNCTION = "main"

  def main(self, text):
    return (text, {})
