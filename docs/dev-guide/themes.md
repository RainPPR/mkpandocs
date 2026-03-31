# 主题开发

MkPandocs 支持自定义主题。

## 使用内置主题

```yaml
theme: mkdocs          # MkDocs 主题
theme: readthedocs     # ReadTheDocs 主题
```

## 自定义主题

### 基本结构

```
my_theme/
├── main.html          # 主模板
├── nav.html           # 导航模板
├── base.html          # 基础模板
└── css/
    └── theme.css      # 样式文件
```

在配置中使用：

```yaml
theme:
  name: null
  custom_dir: my_theme/
```

### 模板变量

主题模板可以使用以下变量：

| 变量 | 说明 |
|------|------|
| `site_name` | 站点名称 |
| `site_url` | 站点 URL |
| `page.title` | 当前页面标题 |
| `page.content` | 当前页面 HTML 内容 |
| `page.toc` | 当前页面目录 |
| `page.url` | 当前页面 URL |
| `nav` | 导航对象 |
| `config` | 完整配置对象 |
| `pages` | 所有页面列表 |

### 主模板示例

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ page.title }} - {{ site_name }}</title>
    <meta charset="utf-8">
    {% for css in extra_css %}
    <link href="{{ css }}" rel="stylesheet">
    {% endfor %}
</head>
<body>
    <nav>
        {% for nav_item in nav %}
        <a href="{{ nav_item.url }}"
           {% if nav_item.active %}class="active"{% endif %}>
            {{ nav_item.title }}
        </a>
        {% endfor %}
    </nav>
    <main>
        <h1>{{ page.title }}</h1>
        {{ page.content }}
    </main>
</body>
</html>
```

### 自定义现有主题

使用 `custom_dir` 在不覆盖主题的情况下添加自定义：

```yaml
theme:
  name: mkdocs
  custom_dir: theme_overrides/
  static_templates:
    - 404.html
```

`custom_dir` 中的文件会覆盖主题中的同名文件。

## Jinja2 模板

MkPandocs 使用 [Jinja2](https://jinja.palletsprojects.com/) 模板引擎。

### 条件渲染

```html
{% if page.toc %}
<nav class="toc">
    {{ page.toc }}
</nav>
{% endif %}
```

### 循环

```html
{% for nav_item in nav %}
<li {% if nav_item.active %}class="active"{% endif %}>
    <a href="{{ nav_item.url }}">{{ nav_item.title }}</a>
</li>
{% endfor %}
```

### 继承

```html
{% extends "base.html" %}

{% block content %}
{{ page.content }}
{% endblock %}
```

## 打包主题

主题可以作为 Python 包分发：

```toml
# pyproject.toml
[project.entry-points."properdocs.themes"]
my-theme = "my_theme"
```
