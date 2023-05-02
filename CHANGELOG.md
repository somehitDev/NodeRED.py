
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
