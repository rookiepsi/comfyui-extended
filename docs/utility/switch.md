# Switch

The `Switch` node switches between multiple inputs based on the condition value.

![Switch](/assets/nodes/utility/switch.png)

## Input

| Name        | Type    | Description                                    |
| ----------- | ------- | ---------------------------------------------- |
| `true`      | ANY     | The input to return if the condition is true.  |
| `false`     | ANY     | The input to return if the condition is false. |
| `condition` | BOOLEAN | The boolean value to evaluate.                 |

## Output

| Name     | Type | Description                                |
| -------- | ---- | ------------------------------------------ |
| `output` | ANY  | The input returned based on the condition. |
