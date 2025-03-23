from .expression import UtilityExpression
from .image_dimensions import UtilityImageDimensions
from .switch import UtilitySwitch

UTILITY_CLASS_MAPPINGS = {
    "UtilityExpression": UtilityExpression,
    "UtilityImageDimensions": UtilityImageDimensions,
    "UtilitySwitch": UtilitySwitch,
}

UTILITY_DISPLAY_NAME_MAPPINGS = {
    "UtilityExpression": "Expression",
    "UtilityImageDimensions": "Image Dimensions",
    "UtilitySwitch": "Switch",
}
