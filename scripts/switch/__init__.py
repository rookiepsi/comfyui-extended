from .image import ImageSwitch
from .mask import MaskSwitch

SWITCH_CLASS_MAPPINGS = {
    "ImageSwitch": ImageSwitch,
    "MaskSwitch": MaskSwitch,
}

SWITCH_DISPLAY_NAME_MAPPINGS = {
    "ImageSwitch": "Image Switch",
    "MaskSwitch": "Mask Switch",
}
