# Expression

The `Expression` node allows you to create dynamic expressions using mathematical operations, string manipulations, statistics/probability functions, and conditional logic.

![Expression](/assets/nodes/utility/expression.png)

## Examples

### Basic Operations

- Add two numbers: `a + b`
- Less than or equal comparison: `a <= b`
- Return true if a or b is true: `a or b`
- Return the larger of a and b: `a if a > b else b`

### Mathematical Functions

- Find minimum value: `min(a, b)`
- Find maximum value: `max(a, b)`
- Round to nearest integer: `round(a)`
- Convert to integer: `int(a)`
- Convert to float: `float(a)`

### String Functions

- Convert to lowercase: `lower("{a}")`
- Convert to uppercase: `upper("{a}")`
- Replace spaces with ", ": `replace("{a}", " ", ", ")`
- Check if b is in a: `contains("{a}", "{b}")`
- Check if a starts with b: `startswith("{a}", "{b}")`

### Statistical and Probability Functions

- Calculate 5! (5×4×3×2×1 = 120): `factorial(5)`
- Return true with 30% probability: `rand() < 0.3`
- Calculate the mean of values a, b, c, and d: `mean([a, b, c, d])`
- Generate a random float between 1 and 1.3 divisible by 0.05 (with clean decimal places): `round(floor(uniform(1, 1.35) / 0.05) * 0.05, 2)`

## Input

| Name         | Type   | Description                 |
| ------------ | ------ | --------------------------- |
| `a`          | ANY    | The first input variable.   |
| `b`          | ANY    | The second input variable.  |
| `c`          | ANY    | The third input variable.   |
| `d`          | ANY    | The fourth input variable.  |
| `expression` | STRING | The expression to evaluate. |

## Output

| Name      | Type    | Description                                           |
| --------- | ------- | ----------------------------------------------------- |
| `INT`     | INT     | The integer value derived from the expression.        |
| `FLOAT`   | FLOAT   | The floating-point value derived from the expression. |
| `STRING`  | STRING  | The string representation of the result.              |
| `BOOLEAN` | BOOLEAN | The boolean representation of the result.             |

## Syntax

Expressions follow standard Python syntax with some important notes about variable access:

- For mathematical and logical operations, you can access variables directly in the expression: `a + b`, `a > b`, etc.
- To access variables in strings, use curly braces: `"Hello {a}"`, `"The sum of {a} and {b} is {a + b}"`, etc.
- Constants `pi`, `e`, `i`, `phi` can be accessed in the expression like any other variables: `a + pi`, `"π = {pi}"`, etc.

## Error Handling

If the input expression contains an error, the node will output `(0, 0.0, error, False)`. To debug expressions, connect the `STRING` output to the `Preview Text` node to see the error.

## Available Constants, Operations and Functions

### Constants

- `pi` - Mathematical constant π (3.14159...).
- `e` - Mathematical constant e (2.71828...).
- `i` - Imaginary unit (√-1).
- `phi` - Golden ratio (1.61803...).

### Arithmetic Operators

- `a + b` - Addition.
- `a - b` - Subtraction.
- `a * b` - Multiplication.
- `a / b` - Division.
- `a // b` - Floor Division.
- `a % b` - Modulus.
- `a ** b` - Power.
- `-a` - Negation.

### Comparison Operators

- `a == b` - Equal.
- `a != b` - Not Equal.
- `a < b` - Less Than.
- `a <= b` - Less Than or Equal.
- `a > b` - Greater Than.
- `a >= b` - Greater Than or Equal.

### Logical Operators

- `a and b` - And.
- `a or b` - Or.
- `not a` - Not.
- `a if b else c` - Conditional.

### Mathematical Functions

- `min(a, b, ...)` - Minimum value.
- `max(a, b, ...)` - Maximum value.
- `round(a)` - Round to nearest integer.
- `sum([a, b, ...])` - Sum of values.
- `abs(a)` - Absolute value.
- `sin(a)` - Sine (radians).
- `cos(a)` - Cosine (radians).
- `tan(a)` - Tangent (radians).
- `sqrt(a)` - Square root.
- `floor(a)` - Floor (round down).
- `ceil(a)` - Ceiling (round up).
- `log(a)` - Natural logarithm.
- `log10(a)` - Base-10 logarithm.
- `exp(a)` - Exponential (e^a).
- `asin(a)` - Arc sine.
- `acos(a)` - Arc cosine.
- `atan(a)` - Arc tangent.
- `sinh(a)` - Hyperbolic sine.
- `cosh(a)` - Hyperbolic cosine.
- `tanh(a)` - Hyperbolic tangent.
- `deg(a)` - Convert radians to degrees.
- `rad(a)` - Convert degrees to radians.
- `real(a)` - Get real part of a complex number.
- `imaginary(a)` - Get imaginary part of a complex number.

### String Functions

- `lower(str)` - Convert to lowercase.
- `upper(str)` - Convert to uppercase.
- `replace(str, old, new)` - Replace substring.
- `split(str, sep)` - Split string into list.
- `join(separator, list)` - Join list into string.
- `strip(str)` - Remove whitespace from ends.
- `lstrip(str, chars)` - Remove whitespace from left.
- `rstrip(str, chars)` - Remove whitespace from right.
- `find(str, sub)` - Find substring position.
- `contains(str, sub)` - Check if substring exists.
- `startswith(str, prefix)` - Check if starts with prefix.
- `endswith(str, suffix)` - Check if ends with suffix.
- `capitalize(str)` - Capitalize first letter.
- `title(str)` - Capitalize each word.
- `reverse(str)` - Reverse string.
- `count(str, sub)` - Count occurrences of substring.
- `zfill(str, width)` - Pad with zeros.
- `isalpha(str)` - Check if all alphabetic.
- `isdigit(str)` - Check if all digits.
- `isalnum(str)` - Check if all alphanumeric.
- `isspace(str)` - Check if all whitespace.
- `islower(str)` - Check if all lowercase.
- `isupper(str)` - Check if all uppercase.

### Regex Functions

- `re_sub(pattern, repl, string, count=0)` - Substitute occurrences of pattern with repl.
- `re_search(pattern, string)` - Search for pattern in string.
- `re_match(pattern, string)` - Match pattern at the start of string.
- `re_findall(pattern, string)` - Find all occurrences of pattern.
- `re_split(pattern, string, maxsplit=0)` - Split string by pattern.
- `re_escape(string)` - Escape special characters in string.

### Statistics and Probability Functions

- `mean(list)` - Calculate arithmetic mean of a list of values.
- `median(list)` - Calculate the median value.
- `mode(list)` - Find the most common value.
- `stdev(list)` - Calculate sample standard deviation.
- `variance(list)` - Calculate sample variance.
- `pstdev(list)` - Calculate population standard deviation.
- `pvariance(list)` - Calculate population variance.
- `normal_pdf(x, mu, sigma)` - Normal probability density function.
- `normal_cdf(x, mu, sigma)` - Normal cumulative distribution function.
- `factorial(n)` - Calculate factorial of n.
- `comb(n, k)` - Number of ways to choose k items from n items without repetition and order.
- `perm(n, k)` - Number of ways to choose k items from n items without repetition with order.
- `random()` - Random float between 0 and 1.
- `randint(a, b)` - Random integer between a and b (inclusive).
- `uniform(a, b)` - Random float between a and b.
- `choice(list)` - Random item from list.
- `gauss(mu, sigma)` - Random value from normal distribution.

### Other Functions

- `int(a)` - Convert to integer.
- `float(a)` - Convert to float.
- `bool(a)` - Convert to boolean.
- `list(a, sep=",")` - Convert string into list with separator (default is comma).
- `len(a)` - Length of a string or list.
