from .blur import rookiepsi_BlurMask
from .construct import rookiepsi_ConstructMask
from .resize import rookiepsi_ResizeMask


MASK_CLASS_MAPPINGS = {
    "rookiepsi_BlurMask": rookiepsi_BlurMask,
    "rookiepsi_ConstructMask": rookiepsi_ConstructMask,
    "rookiepsi_ResizeMask": rookiepsi_ResizeMask,
}

MASK_DISPLAY_NAME_MAPPINGS = {
    "rookiepsi_BlurMask": "Blur Mask",
    "rookiepsi_ConstructMask": "Construct Mask",
    "rookiepsi_ResizeMask": "Resize Mask",
}
