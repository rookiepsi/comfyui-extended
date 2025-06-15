from .blur import rookiepsi_BlurMask
from .construct import rookiepsi_ConstructMask


MASK_CLASS_MAPPINGS = {
    "rookiepsi_BlurMask": rookiepsi_BlurMask,
    "rookiepsi_ConstructMask": rookiepsi_ConstructMask,
}

MASK_DISPLAY_NAME_MAPPINGS = {
    "rookiepsi_BlurMask": "Blur Mask",
    "rookiepsi_ConstructMask": "Construct Mask",
}
