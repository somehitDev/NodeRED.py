<h1 align="center">
    NodeRED.py
</h1>
<p align="center">
    make python function to Node-RED node
</p>
<br/>

<div align="center">
    <a href="https://github.com/oyajiDev/HU4PY/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/oyajiDev/HU4PY.svg" alt="MIT License" />
    </a>
    <a href="https://pypi.org/project/nodered.py/">
        <img src="https://img.shields.io/pypi/v/nodered.py.svg" alt="pypi" />
    </a>
</div>
<br/><br/>

## 🎛️ requirements
- node.js 18.16.1 or higher(latest stable)
  - nodered.py 0.2.6 or higher, automatically download from internet if no node.js installed
- python 3.7 or higher
- tested on

|        OS       | Tested | Pass |
| --------------- | ------ | ---- |
| Mac 13(Ventura) |   ✅   |  ✅  |
| Windows 10      |   ✅   |  ✅  |
| Linux(WSL)      |   🚫   |      |

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
    .set_port(port).build()

# using RED directly
red = RED(
    "{user_dir}", "{node_red_dir}",
    "{admin_root}", "{node_root}", port, "{default_flow}",
    remote_access, default_category_visible
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

<br>

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

<br/>

### start Node-RED
```python
red.start({debug:bool}, {callback:MethodType})
```
<br/><br/>

## Todos
✅ type support for "list" and "dict"

<br/><br/>

## Roadmap To 2.0
✅ remove aiohttp server

🟩 flexible property ui
