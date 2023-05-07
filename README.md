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
from noderedpy import RED

red = RED(
    os.path.join(__dirname, ".node-red"),
    os.path.join(__dirname, "node_red_dir"),
    "/node-red", 1880
)
```

<br/>

### register Node
- register as decorator
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/08b2295ab537be97ad9e9a2f94154cdcb36685d0/noderedpy/decorator.py#L8">noredpy.decorator.register function</a> for details
```python
from noderedpy.decorator import register

@register("test")
def test(props:dict, msg:dict) -> dict:
    # user codes here
    return msg
```
- register from Node-RED object
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/c205b617296d3ef14e93f08e72657fd41ab8d081/noderedpy/_nodered.py#L85">noredpy.decorator.register function</a> for details
```python
api = API()

red.register("test", api.test)
```
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/08b2295ab537be97ad9e9a2f94154cdcb36685d0/noderedpy/_property.py">noderedpy._property</a> for details of "Property"

<br/>

### start Node-RED
```python
red.start({debug:bool}, {callback:MethodType})
```
<br/><br/>

## Todos
[x] type support for "list" and "dict"

<br/><br/>

## Roadmap To 2.0
[x] remove aiohttp server

[ ] flexible property ui
