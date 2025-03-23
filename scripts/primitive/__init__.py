from .boolean import PrimitiveBoolean
from .dimensions import PrimitiveDimensions
from .float import PrimitiveFloat
from .integer import PrimitiveInteger
from .text import PrimitiveText

PRIMITIVE_CLASS_MAPPINGS = {
    "PrimitiveBoolean": PrimitiveBoolean,
    "PrimitiveDimensions": PrimitiveDimensions,
    "PrimitiveFloat": PrimitiveFloat,
    "PrimitiveInteger": PrimitiveInteger,
    "PrimitiveText": PrimitiveText,
}

PRIMITIVE_DISPLAY_NAME_MAPPINGS = {
    "PrimitiveBoolean": "Boolean",
    "PrimitiveDimensions": "Dimensions",
    "PrimitiveFloat": "Float",
    "PrimitiveInteger": "Integer",
    "PrimitiveText": "Text",
}
