import ast
import math
import operator
import random
import re
import statistics


class AnyType(str):
  def __ne__(self, __value: object) -> bool:
    return False

  def __call__(self, *args, **kwargs):
    return self


any = AnyType("*")

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda x, y: x and y,
    ast.Or: lambda x, y: x or y,
    ast.Not: operator.not_
}

SAFE_FUNCTIONS = {
    # Math functions
    "min": min,
    "max": max,
    "round": round,
    "sum": sum,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "floor": math.floor,
    "ceil": math.ceil,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "deg": math.degrees,
    "rad": math.radians,
    "real": lambda x: x.real if isinstance(x, complex) else x,
    "imaginary": lambda x: x.imag if isinstance(x, complex) else 0,

    # String functions
    "lower": lambda s: str(s).lower(),
    "upper": lambda s: str(s).upper(),
    "replace": lambda s, old, new: str(s).replace(old, new),
    "split": lambda s, sep=None: str(s).split(sep),
    "join": lambda sep, lst: sep.join(str(x) for x in lst) if isinstance(lst, (list, tuple)) else str(lst),
    "strip": lambda s: str(s).strip(),
    "lstrip": lambda s, chars=None: str(s).lstrip(chars),
    "rstrip": lambda s, chars=None: str(s).rstrip(chars),
    "find": lambda s, sub: str(s).find(sub),
    "contains": lambda s, sub: sub in str(s),
    "startswith": lambda s, prefix: str(s).startswith(prefix),
    "endswith": lambda s, suffix: str(s).endswith(suffix),
    "capitalize": lambda s: str(s).capitalize(),
    "title": lambda s: str(s).title(),
    "reverse": lambda s: str(s)[::-1],
    "count": lambda s, sub: str(s).count(sub),
    "zfill": lambda s, width: str(s).zfill(width),
    "isalpha": lambda s: str(s).isalpha(),
    "isdigit": lambda s: str(s).isdigit(),
    "isalnum": lambda s: str(s).isalnum(),
    "isspace": lambda s: str(s).isspace(),
    "islower": lambda s: str(s).islower(),
    "isupper": lambda s: str(s).isupper(),

    # Regex functions
    "re_sub": lambda pattern, repl, string, count=0: re.sub(pattern, repl, string, count=count),
    "re_search": lambda pattern, string: bool(re.search(pattern, string)),
    "re_match": lambda pattern, string: bool(re.match(pattern, string)),
    "re_findall": lambda pattern, string: re.findall(pattern, string),
    "re_split": lambda pattern, string, maxsplit=0: re.split(pattern, string, maxsplit),
    "re_escape": lambda string: re.escape(string),

    # Statistics and probability functions
    "mean": statistics.mean,
    "median": statistics.median,
    "mode": statistics.mode,
    "stdev": statistics.stdev,
    "variance": statistics.variance,
    "pvariance": statistics.pvariance,
    "pstdev": statistics.pstdev,
    "normal_pdf": lambda x, mu=0, sigma=1: (1/(sigma * math.sqrt(2*math.pi))) * math.exp(-0.5 * ((x-mu)/sigma)**2),
    "normal_cdf": lambda x, mu=0, sigma=1: 0.5 * (1 + math.erf((x-mu)/(sigma*math.sqrt(2)))),
    "factorial": math.factorial,
    "comb": math.comb,
    "perm": math.perm,
    "random": random.random,
    "randint": random.randint,
    "uniform": random.uniform,
    "choice": random.choice,
    "gauss": random.gauss,

    # Other functions
    "int": int,
    "float": float,
    "bool": bool,
    "list": lambda s, sep=",": [x.strip() for x in str(s).split(sep)],
    "len": len,
}


class SafeEvaluator:
  def __init__(self, variables=None, functions=None):
    self.variables = variables or {}
    self.functions = functions or {}

  def eval(self, expr):
    try:
      parsed = ast.parse(expr, mode="eval")
      return self._evaluate_node(parsed.body)
    except SyntaxError as e:
      raise ValueError(f"Syntax error: {e}")

  def _evaluate_node(self, node):
    # Simple values
    if isinstance(node, ast.Constant):
      return node.value

    # Variable names
    elif isinstance(node, ast.Name):
      if node.id in self.variables:
        return self.variables[node.id]
      raise ValueError(f"Unknown variable: {node.id}")

    # Binary operations (a + b, a - b, etc.)
    elif isinstance(node, ast.BinOp):
      left = self._evaluate_node(node.left)
      right = self._evaluate_node(node.right)

      if type(node.op) not in OPERATORS:
        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")

      return OPERATORS[type(node.op)](left, right)

    # Unary operations (-a, not a, etc.)
    elif isinstance(node, ast.UnaryOp):
      operand = self._evaluate_node(node.operand)

      if type(node.op) not in OPERATORS:
        raise ValueError(
            f"Unsupported unary operator: {type(node.op).__name__}")

      return OPERATORS[type(node.op)](operand)

    # Comparisons (a > b, a == b, etc.)
    elif isinstance(node, ast.Compare):
      left = self._evaluate_node(node.left)

      for op, comparator in zip(node.ops, node.comparators):
        right = self._evaluate_node(comparator)

        if type(op) not in OPERATORS:
          raise ValueError(
              f"Unsupported comparison operator: {type(op).__name__}")

        if not OPERATORS[type(op)](left, right):
          return False

        left = right

      return True

    # Boolean operations (and, or)
    elif isinstance(node, ast.BoolOp):
      if isinstance(node.op, ast.And):
        for value in node.values:
          if not bool(self._evaluate_node(value)):
            return False
        return True
      else:
        for value in node.values:
          if bool(self._evaluate_node(value)):
            return True
        return False

    # Function calls
    elif isinstance(node, ast.Call):
      if isinstance(node.func, ast.Name):
        func_name = node.func.id

        if func_name not in self.functions:
          raise ValueError(f"Unknown or unsupported function: {func_name}")

        args = [self._evaluate_node(arg) for arg in node.args]
        kwargs = {kw.arg: self._evaluate_node(
            kw.value) for kw in node.keywords}

        return self.functions[func_name](*args, **kwargs)

      elif isinstance(node.func, ast.Attribute):
        obj = self._evaluate_node(node.func.value)
        method_name = node.func.attr

        if method_name.startswith("__"):
          raise ValueError(
              f"Access to magic methods is not allowed: {method_name}")

        if isinstance(obj, str) and hasattr(str, method_name):
          method = getattr(obj, method_name)

          if callable(method):
            args = [self._evaluate_node(arg) for arg in node.args]
            kwargs = {kw.arg: self._evaluate_node(
                kw.value) for kw in node.keywords}
            return method(*args, **kwargs)

        raise ValueError(f"Unsupported method call: {method_name}")

      raise ValueError(f"Unsupported function call type")

    # Conditional expressions (a if b else c)
    elif isinstance(node, ast.IfExp):
      condition = self._evaluate_node(node.test)
      return self._evaluate_node(node.body if condition else node.orelse)

    # List literals
    elif isinstance(node, ast.List):
      return [self._evaluate_node(elt) for elt in node.elts]

    # Dictionary literals
    elif isinstance(node, ast.Dict):
      return {
          self._evaluate_node(k): self._evaluate_node(v)
          for k, v in zip(node.keys, node.values)
      }

    # Subscripting (a[b])
    elif isinstance(node, ast.Subscript):
      value = self._evaluate_node(node.value)

      if isinstance(node.slice, ast.Constant):
        index = node.slice.value
        if isinstance(value, (list, tuple, str)) and isinstance(index, int):
          if 0 <= index < len(value):
            return value[index]
          else:
            raise ValueError(
                f"Index {index} out of range for sequence of length {len(value)}")
        elif isinstance(value, dict) and index in value:
          return value[index]
        else:
          raise ValueError(
              f"Invalid index type or container type for subscript operation")
      elif isinstance(node.slice, ast.Slice):
        lower = self._evaluate_node(
            node.slice.lower) if node.slice.lower else None
        upper = self._evaluate_node(
            node.slice.upper) if node.slice.upper else None
        step = self._evaluate_node(
            node.slice.step) if node.slice.step else None
        if isinstance(value, (list, tuple, str)):
          try:
            return value[lower:upper:step]
          except Exception as e:
            raise ValueError(f"Invalid slice parameters: {e}")
        else:
          raise ValueError(f"Cannot apply slice to {type(value).__name__}")
      else:
        try:
          index = self._evaluate_node(node.slice)

          if isinstance(value, (list, tuple, str)):
            if isinstance(index, int):
              if -len(value) <= index < len(value):
                return value[index]
              else:
                raise ValueError(
                    f"Index {index} out of range for sequence of length {len(value)}")
            else:
              raise ValueError(
                  f"Index must be an integer, got {type(index).__name__}")
          elif isinstance(value, dict):
            if index in value:
              return value[index]
            else:
              raise ValueError(f"Key {index} not found in dictionary")
          else:
            raise ValueError(f"Cannot index into {type(value).__name__}")
        except Exception as e:
          raise ValueError(f"Invalid subscript operation: {str(e)}")

    else:
      raise ValueError(f"Unsupported expression type: {type(node).__name__}")


class UtilityExpression:
  @classmethod
  def INPUT_TYPES(cls):
    return {
        "required": {
            "expression": ("STRING", {"default": "", "multiline": True, "placeholder": "Read the docs at https://github.com/rookiepsi/comfyui-extended to learn how to write expressions."}),
        },
        "optional": {
            "a": (any, {}),
            "b": (any, {}),
            "c": (any, {}),
            "d": (any, {})
        }
    }

  RETURN_TYPES = ("INT", "FLOAT", "STRING", "BOOLEAN")
  FUNCTION = "main"
  CATEGORY = "comfyui-extended/utility"

  @staticmethod
  def normalize_input(value):
    if hasattr(value, "shape"):
      return list(value.shape)

    if isinstance(value, bool):
      return value

    if isinstance(value, str):
      if value.lower() in ("true", "false"):
        return value.lower() == "true"
      try:
        return float(value)
      except ValueError:
        pass

    return value

  def evaluate_expression(self, expression, a, b, c, d):
    try:
      normalized_a = self.normalize_input(a)
      normalized_b = self.normalize_input(b)
      normalized_c = self.normalize_input(c)
      normalized_d = self.normalize_input(d)

      variables = {
          "a": normalized_a,
          "b": normalized_b,
          "c": normalized_c,
          "d": normalized_d,
          "pi": math.pi,
          "e": math.e,
          "i": complex(0, 1),
          "phi": (1 + math.sqrt(5)) / 2,
      }

      if any(f"{{{var}}}" in expression for var in ["a", "b", "c", "d", "pi", "e", "i", "phi"]):
        replacements = {
            "{a}": str(a),
            "{b}": str(b),
            "{c}": str(c),
            "{d}": str(d),
            "{pi}": str(math.pi),
            "{e}": str(math.e),
            "{i}": str(complex(0, 1)),
            "{phi}": str((1 + math.sqrt(5)) / 2)
        }

        for placeholder, value in replacements.items():
          expression = expression.replace(placeholder, value)

      expression = expression.replace("__", "_")

      evaluator = SafeEvaluator(
          variables=variables,
          functions=SAFE_FUNCTIONS
      )

      result = evaluator.eval(expression)
      return result, None

    except Exception as e:
      error = f"Error evaluating expression: {str(e)}"
      print(error)
      return 0, error

  @classmethod
  def IS_CHANGED(cls, expression, **kwargs):
    if re.search(r"\b(random|randint|uniform|choice|gauss)\b", expression):
      return int("NaN")
    else:
      return expression

  def main(self, expression, a=None, b=None, c=None, d=None):
    if not expression.strip():
      return (0, 0.0, "", False)

    result, error = self.evaluate_expression(expression, a, b, c, d)

    if error:
      return (0, 0.0, f"{error}", False)

    if result is None:
      return (0, 0.0, "", False)

    if isinstance(result, bool):
      return (1, 1.0, "true", True) if result else (0, 0.0, "false", False)

    elif isinstance(result, (int, float)):
      if isinstance(result, float) and math.isnan(result):
        return (0, 0.0, "", False)
      return (int(round(float(result))), float(result), str(result), bool(result))

    elif isinstance(result, str):
      try:
        num = float(result)
        return (int(round(num)), num, result, bool(result))
      except ValueError:
        return (0, 0.0, result, False)

    else:
      return (0, 0.0, str(result), False)
