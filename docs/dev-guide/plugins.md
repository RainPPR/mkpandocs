# 插件开发

MkPandocs 支持通过插件扩展功能。

## 使用插件

在 `mkpandocs.yml` 中启用插件：

```yaml
plugins:
  - search
  - my-plugin:
      option1: value1
```

## 开发插件

插件是 Python 类，继承自 `properdocs.plugins.BasePlugin`。

### 基本结构

```python
from properdocs.plugins import BasePlugin
from properdocs.config import config_options as c


class MyPluginConfig(properdocs.config.base.Config):
    my_option = c.Type(str, default='default_value')


class MyPlugin(BasePlugin[MyPluginConfig]):
    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        # 在 Markdown 渲染前处理
        return markdown

    def on_page_content(self, html, page, config, files, **kwargs):
        # 在 HTML 渲染后处理
        return html
```

### 事件

插件通过定义事件处理函数来响应构建过程中的各个阶段。

#### on_config

在配置加载完成后调用。

```python
def on_config(self, config, **kwargs):
    # 可以修改配置
    return config
```

#### on_files

在文件收集完成后调用。

```python
def on_files(self, files, config, **kwargs):
    # 可以添加或移除文件
    return files
```

#### on_nav

在导航构建完成后调用。

```python
def on_nav(self, nav, config, files, **kwargs):
    # 可以修改导航结构
    return nav
```

#### on_page_read_source

在读取页面源文件时调用。

```python
def on_page_read_source(self, page, config, **kwargs):
    # 可以返回自定义的 Markdown 内容
    return None  # 返回 None 使用文件内容
```

#### on_page_markdown

在 Markdown 渲染为 HTML 之前调用。

```python
def on_page_markdown(self, markdown, page, config, files, **kwargs):
    # 修改 Markdown 内容
    return markdown
```

#### on_page_content

在 Markdown 渲染为 HTML 之后调用。

```python
def on_page_content(self, html, page, config, files, **kwargs):
    # 修改 HTML 内容
    return html
```

#### on_page_context

在页面模板渲染之前调用。

```python
def on_page_context(self, context, page, config, nav, **kwargs):
    # 修改模板上下文
    return context
```

#### on_post_build

在构建完成后调用。

```python
def on_post_build(self, config, **kwargs):
    # 执行构建后操作
    pass
```

### 发布插件

插件应该作为 Python 包发布，并通过 entry_points 注册：

```toml
# pyproject.toml
[project.entry-points."properdocs.plugins"]
my-plugin = "my_package.plugin:MyPlugin"
```

### 简易插件（hooks）

对于简单的用例，不需要完整的插件包。可以在 `mkpandocs.yml` 中使用 `hooks`：

```yaml
hooks:
  - my_hooks.py
```

`my_hooks.py` 中直接定义事件处理函数（不需要类和 `self`）：

```python
def on_page_markdown(markdown, page, **kwargs):
    return markdown.replace('foo', 'bar')
```
