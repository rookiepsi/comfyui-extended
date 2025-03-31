import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
  name: "Comfy.ExtendedPreview",

  setup() {
    api.addEventListener("comfyui-extended_preview", ({ detail }) => {
      const { id, value } = detail;

      const node = app.graph._nodes_by_id[id];
      if (!node) return;

      node._previewWidget.inputEl.value = value;
    });
  },
});
