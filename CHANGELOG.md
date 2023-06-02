
## version 0.1.0
- Initial Release

<br/>

## version 0.1.1
- type support for "list" and "dict"
- add "display_icon" parameter to "NodeProperty"
  - if None, set icon by "type" of property

<br/>

## version 0.1.2
- divide "NodeProperty" to multiple Property classes
  - for input, InputProperty
  - for list, ListProperty
  - for dict(json), DictProperty
  - for spinner, SpinnerProperty
  - for combobox, ComboBoxProperty

<br/>

## version 0.1.3
- create template files
- remove unnecessary code
- apply "min", "max", "step" of "SpinnerProperty" correctly
- add "height" to "ListProperty", "DictProperty"

<br/>

## version 0.1.4
- create "CodeProperty"
- "DictProperty" inherits "CodeProperty" with "json" language setting

<br/>

## version 0.2.0
- add <a href="https://github.com/oyajiDev/NodeRED.py/blob/deea7530d6fcda9cdf6d76e9b5f827064de5722c/noderedpy/_nodered.py#L60">editorTheme</a>
- remove server.
  - start Node-RED object directly.
- remove standalone server.
  - pywebview integration is in <a href="https://github.com/oyajiDev/NodeRED.py/blob/master/tests/pywebview_test.py">tests</a>.

<br/>

## version 0.2.1
- remove unnecessary code
- add "version", "description", "author", "keywords", "icon" to Node attributes.
- remove "nodered-py-" prefix from Node name.
  - "nodered-py-" only attach to directory of Node.

<br>

## version 0.2.2
- change node-red command arguments to config.json.
- add <a href="https://github.com/oyajiDev/NodeRED.py/blob/master/tests/pywebview_test.py">"auths"</a> options.
