from .liquify import ImageLiquify
from .crop import rookiepsi_CropImageToMask

IMAGE_CLASS_MAPPINGS = {
    "ImageLiquify": ImageLiquify,
    "rookiepsi_CropImageToMask": rookiepsi_CropImageToMask,
}

IMAGE_DISPLAY_NAME_MAPPINGS = {
    "ImageLiquify": "Liquify Image",
    "rookiepsi_CropImageToMask": "Crop Image To Mask",
}
