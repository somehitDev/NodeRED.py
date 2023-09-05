# -*- coding: utf-8 -*-
import json


def node_html(name:str, icon:str, category:str, color:str, html:str, props:dict, prepare:str, cancel:str, save:str) -> str:
    return """
<script type="text/html" data-template-name="{$name}">
    <style>
        .form-row label {
            width: auto !important;
        }
        .form-row span.ui-spinner {
            width: 100%;
        }
        .form-row[data-flex="true"] span.ui-spinner {
            flex: 1;
        }
    </style>
{$html}
</script>

<script type="text/javascript">
    RED.nodes.registerType("{$name}", {
        category: "{$category}",
        color: "{$color}",
        defaults: {$props},
        inputs: 1, outputs: 1,
        icon: "{$icon}",
        label: function() {
            return this.name || "{$name}";
        },
        oneditprepare: function() {
            var node = this;
{$prepare}
        },
        oneditcancel: function() {
            var node = this;
{$cancel}
        },
        oneditsave: function() {
            var node = this;
{$save}
        }
    });
</script>
""".replace("{$name}", name).replace("{$icon}", icon)\
    .replace("{$category}", category).replace("{$color}", color)\
    .replace("{$html}", html)\
    .replace("{$props}", json.dumps(props, indent = 4))\
    .replace("{$prepare}", prepare)\
    .replace("{$cancel}", cancel)\
    .replace("{$save}", save)
