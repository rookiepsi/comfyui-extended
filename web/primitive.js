import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
  name: "Comfy.ExtendedPrimitive",

  async setup() {
    const ids = [];

    const methods = {
      increment: (value, step, min, max) => {
        return Math.min(max, Math.max(min, value + step));
      },
      decrement: (value, step, min, max) => {
        return Math.min(max, Math.max(min, value - step));
      },
      randomize: {
        integer: (step, min, max) => {
          const steps = Math.floor((max - min) / step) + 1;
          return min + Math.floor(Math.random() * steps) * step;
        },
        float: (step, min, max) => {
          const steps = Math.floor((max - min) / step);
          const value = min + Math.floor(Math.random() * (steps + 1)) * step;
          const precision = Math.max(0, -Math.floor(Math.log10(step)));
          return Number(value.toFixed(precision));
        },
        boolean: () => Math.random() >= 0.5,
      },
    };

    api.addEventListener("comfyui-extended_primitive", ({ detail }) => {
      const { id, value, method, type } = detail;

      const node = app.graph._nodes_by_id[id];
      if (!node) return;

      if (!ids.includes(id)) {
        ids.push(id);
      }

      const widget = node.widgets.find((w) => w.name === "value");

      switch (method) {
        case "fixed":
          return;
        case "previous":
          widget.value = value;
          return;
        case "randomize":
          if (type === "boolean") {
            widget.value = methods.randomize.boolean();
          } else {
            const { step, range } = detail;
            widget.value = methods.randomize[type](step, range.min, range.max);
          }
          return;
        default: {
          const { step, range } = detail;
          widget.value = methods[method](value, step, range.min, range.max);
        }
      }
    });
  },
});
