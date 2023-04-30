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
### server initialize
- default server
```python
from noderedpy import Server, RED

server = Server(
    RED(
        os.path.join(__dirname, ".node-red"),
        "/node-red", 1880
    )
)
```
- standalone(with webview)
```python
from noderedpy import StandaloneServer, RED

server = StandaloneServer(
    RED(
        os.path.join(__dirname, ".node-red"),
        "/node-red", 1880
    )
)
```
<br/>

### register Node
```python
@register("test")
def test(props:dict, msg:dict) -> dict:
    # user codes here
    return msg
```
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/08b2295ab537be97ad9e9a2f94154cdcb36685d0/noderedpy/decorator.py#L8">noredpy.decorator.register function</a> for details
- See <a href="https://github.com/oyajiDev/NodeRED.py/blob/08b2295ab537be97ad9e9a2f94154cdcb36685d0/noderedpy/_property.py">noderedpy._property</a> for details of "Property"
<br/>

### start server
- default server
```python
server.start("{port}")
```
- standalone(with webview)
```python
server.start("{title}")
```
<br/><br/>

## Todos
[x] type support for "list" and "dict"
