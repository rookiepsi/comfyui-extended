from .boolean import PreviewBoolean
from .float import PreviewFloat
from .integer import PreviewInteger
from .mask import PreviewMask
from .text import PreviewText

PREVIEW_CLASS_MAPPINGS = {
    "PreviewBoolean": PreviewBoolean,
    "PreviewFloat": PreviewFloat,
    "PreviewInteger": PreviewInteger,
    "PreviewMask": PreviewMask,
    "PreviewText": PreviewText,
}

PREVIEW_DISPLAY_NAME_MAPPINGS = {
    "PreviewBoolean": "Preview Boolean",
    "PreviewFloat": "Preview Float",
    "PreviewInteger": "Preview Integer",
    "PreviewMask": "Preview Mask",
    "PreviewText": "Preview Text",
}
