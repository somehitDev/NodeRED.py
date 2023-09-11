<h1 align="center">
    NodeRED.py
</h1>
<p align="center">
    make python function to Node-RED node
</p>
<br/>

<div align="center">
    <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue" />
    <br>
    <a href="https://github.com/oyajiDev/NodeRED.py/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/oyajiDev/NodeRED.py.svg" alt="MIT License" />
    </a>
    <a href="https://pypi.org/project/nodered.py/">
        <img src="https://img.shields.io/pypi/v/nodered.py.svg" alt="pypi" />
    </a>
</div>
<br/><br/>

## 🎛️ requirements
- Node-RED 3.x
- node.js 16.x or higher(tested unto 18.x)
  - nodered.py 0.2.6 or higher, automatically download from internet if no node.js installed
- python 3.7 or higher
- tested on

|        OS       | Tested | Pass |
| --------------- | ------ | ---- |
| Mac 13(Ventura) |   ✅   |  ✅  |
| Windows 10      |   ✅   |  ✅  |
| Linux(RPI/ARM)  |   ✅   |  ✅  |

<br/><br/>

## 🌐 install
### - using pip
```zsh
python -m pip install nodered.py
```

### - using git(dev)
```zsh
python -m pip install git+https://github.com/oyajiDev/NodeRED.py.git
```

<br/><br/>

## 🛠 usage
### Node-RED initialize
```python
from noderedpy import REDBuilder, RED, Auth

# using builder
red = REDBuilder()\
    .set_user_dir("{user_dir}")\
    .set_node_red_dir("{node_red_dir}")\
    .set_admin_root("{admin_root}")\
    .set_node_root("{node_root}")\
    .set_port(port)\
    .set_default_flow("{default_flow}")\
    .set_remote_access(remote_access)\
    .set_default_categories([{default_categories}])\
    .set_node_globals({global_variables})\
    .build()

# using RED directly
red = RED(
    "{user_dir}", "{node_red_dir}",
    "{admin_root}", "{node_root}", port, "{default_flow}",
    remote_access, [{default_categories}],
    {global_variables}
)

# change editor theme settings
red.editor_theme.palette.editable = False
red.editor_theme.projects.enabled = False

# add auths
red.node_auths.append(
    Auth(username = "node-red-py", password = "p@ssword")
)
```

<br/>

### register Node
#### register as decorator
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/08b2295ab537be97ad9e9a2f94154cdcb36685d0/noderedpy/decorator.py#L8">noredpy.decorator.register function</a> for details
```python
from noderedpy import Node
from noderedpy.decorator import register

@register("test")
def test(node:Node, props:dict, msg:dict) -> dict:
    # user codes here
    return msg
```
#### register from Node-RED object
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/c205b617296d3ef14e93f08e72657fd41ab8d081/noderedpy/_nodered.py#L85">noredpy.decorator.register function</a> for details
```python
api = API()

red.register("test", api.test)
```
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/08b2295ab537be97ad9e9a2f94154cdcb36685d0/noderedpy/_property.py">noderedpy._property</a> for details of "Property"
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/master/tests/server_test.py">example</a> for details.

<br/>

### custom Property/Widget
```python
import htmlgenerator as hg
from noderedpy.nodered.node.properties.property import Property, RenderedProperty
from noderedpy.nodered.red.editor.widget import Widget, RenderedWidget

# custom property
class MyProperty(Property):
    def __init__(self):
        super().__init__(**{property_kwargs})

    def render(self) -> RenderedProperty:
        # abstract method for node creation
        return RenderedProperty(**{kwargs})

# custom widget
class MyWidget(Widget):
    def __init__(self):
        super().__init__(**{widget_kwargs})

    def render(self) -> RenderedWidget:
        # abstract method for node creation
        return RenderedWidget(**{kwargs})
```

<br/>

### register route
#### route(get, post)
- register as decorator
```python
from noderedpy.decorator import route

# get
@route("{route_url}", "get")
def route1(params:dict) -> dict:
    return {}

# post
@route("{route_url}", "post")
def route1(datas:dict) -> dict:
    return {}
```
- register from Node-RED object
```python
# get
red.route(lambda params: {}, "{route_url}", "get")

# post
red.route(lambda datas: {}, "{route_url}", "post")
```

#### static
```python
red.static("/static", "{static_directory_or_file_path}")
```

### custom editor widget
```python
from noderedpy.nodered.red.editor.widget import Widget, RenderedWidget

class MyWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def render(self) -> RenderedWidget:
        return RenderedWidget()
```
- see pre-made <a href="https://github.com/oyajiDev/NodeRED.py/tree/master/noderedpy/nodered/node/properties">Properties</a> or <a href="https://github.com/oyajiDev/NodeRED.py/tree/master/noderedpy/nodered/red/editor/ui">Widgets</a> for details.

<br/>

### start Node-RED
```python
red.start({debug:bool}, {callback:MethodType})
```
<br/><br/>

## Todos
✅ type support for "list" and "dict"

<br/><br/>

## Roadmap To 0.2.0
✅ remove aiohttp server

## Roadmap to 0.3.0
✅ add Tab.

🟩 more property types.(processing...)
  - ✅ TypedInput
  - 🟩 SearchBox
  - 🟩 TreeList
