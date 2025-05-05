import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
  name: "Comfy.Extended",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.category?.startsWith("comfyui-extended/utility")) {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated?.apply(this, arguments);

        if (nodeType.comfyClass === "UtilityExpression") {
          this.size[0] = 375;
        }

        if (nodeType.comfyClass === "UtilityImageDimensions") {
          this.size[0] = 225;
        }

        if (nodeType.comfyClass === "UtilitySwitch") {
          this.size[0] = 300;
        }
      };
    }

    if (nodeData.category?.startsWith("comfyui-extended/preview")) {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated?.apply(this, arguments);

        if (nodeType.comfyClass === "PreviewMask") {
          this.size[0] = 225;
          return;
        }

        this._previewWidget = ComfyWidgets["STRING"](
          this,
          "preview",
          ["STRING", { multiline: true }],
          app
        ).widget;

        this._previewWidget.inputEl.readOnly = true;

        if (nodeType.comfyClass === "PreviewText") {
          this.size[0] = 300;
          this.size[1] = 125;
        } else {
          this.size[0] = 225;
          this.size[1] = 112;
        }
      };
    }

    if (nodeData.category === "comfyui-extended/primitive") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated?.apply(this, arguments);

        this.size[0] = 300;

        if (nodeType.comfyClass === "PrimitiveText") {
          this.size[1] = 125;
        }

        if (nodeType.comfyClass === "PrimitiveDimensions") {
          this.size[1] = 150;
        }
      };
    }

    if (nodeData.category === "comfyui-extended/switch") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated?.apply(this, arguments);

        this.size[0] = 300;
      };
    }
  },
});
