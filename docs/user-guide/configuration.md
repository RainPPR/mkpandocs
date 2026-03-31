# 配置

MkPandocs 通过项目根目录下的 `mkpandocs.yml` 文件进行配置。所有配置项均可选，但 `site_name` 是唯一必须设置的项。

## 基本配置

### site_name

文档站点的标题，这是唯一的必填配置。

```yaml
site_name: 我的项目文档
```

### site_url

站点的完整 URL，用于生成 canonical 链接。

```yaml
site_url: https://example.com/docs/
```

### site_description

站点描述，会添加到 HTML 的 meta 标签中。

```yaml
site_description: 我的项目文档
```

### site_author

作者名称，会添加到 HTML 的 meta 标签中。

```yaml
site_author: 作者名称
```

### copyright

版权信息，显示在页面底部。

```yaml
copyright: Copyright &copy; 2026 MyName
```

## 文档布局

### nav

定义站点导航结构。路径相对于 `docs_dir`。

```yaml
nav:
  - 首页: index.md
  - 指南:
    - 快速开始: guide/getting-started.md
    - 配置: guide/configuration.md
  - API: api/reference.md
```

如果未设置 `nav`，MkPandocs 会自动从 `docs_dir` 中收集所有 Markdown 文件生成导航。

### docs_dir

文档源文件目录。

```yaml
docs_dir: docs
```

**默认值**：`docs`

### site_dir

构建输出目录。

```yaml
site_dir: site
```

**默认值**：`site`

### exclude_docs

使用 `.gitignore` 格式的模式排除文件。

```yaml
exclude_docs: |
  *.py
  drafts/
```

### draft_docs

标记为草稿的文件，在 `serve` 时可用但不会包含在构建中。

```yaml
draft_docs: |
  drafts/
  *_draft.md
```

## Pandoc 配置

所有 Pandoc 相关配置都在 `pandoc` 嵌套节点下。

```yaml
pandoc:
  format: markdown+raw_html+raw_attribute
  to: html5
  args: []
  filters: []
  lua_filters: []
  keep_frontmatter: false
  html_parser: html.parser
  json_filters: []
```

### pandoc.format

Pandoc 的输入格式。

```yaml
pandoc:
  format: markdown+raw_html+raw_attribute
```

**默认值**：`markdown`

常用扩展：

- `raw_html` — 允许内联 HTML
- `raw_attribute` — 允许原始属性语法
- `tex_math_dollars` — 支持 `$...$` 数学公式
- `fenced_code_blocks` — 支持围栏代码块
- `backtick_code_blocks` — 支持反引号代码块

### pandoc.to

Pandoc 的输出格式。

```yaml
pandoc:
  to: html5
```

**默认值**：`html5`

### pandoc.args

传递给 Pandoc 的额外参数。

```yaml
pandoc:
  args:
    - --wrap=none
    - --number-sections
```

### pandoc.filters

Pandoc 过滤器列表（外部程序，通过 JSON 与 Pandoc 通信）。

```yaml
pandoc:
  filters:
    - pandoc-crossref
```

### pandoc.lua_filters

Lua 过滤器列表，路径相对于当前工作目录。

```yaml
pandoc:
  lua_filters:
    - filters/link_class.lua
```

### pandoc.keep_frontmatter

是否保留 YAML frontmatter。设为 `False` 时会剥离 frontmatter（与标准 MkDocs 行为一致）。

```yaml
pandoc:
  keep_frontmatter: false
```

**默认值**：`false`

### pandoc.html_parser

BeautifulSoup 使用的 HTML 解析器。

```yaml
pandoc:
  html_parser: html.parser
```

可选值：`html.parser`（Python 内置）、`lxml`、`html5lib`

**默认值**：`html.parser`

### pandoc.json_filters

JSON AST 过滤器列表。每个过滤器是一个 Python 脚本，通过 stdin 接收 Pandoc JSON AST，处理后通过 stdout 输出。详见 [JSON 过滤器](json-filters.md)。

```yaml
pandoc:
  json_filters:
    - filters/add_target_blank.py
```

## 主题

### theme

设置文档主题。

```yaml
# 使用内置主题
theme: mkdocs

# 使用带配置的主题
theme:
  name: material
  language: zh
  palette:
    - scheme: default
      primary: indigo
  features:
    - navigation.instant
    - search.highlight
```

## 插件

### plugins

启用的插件列表。

```yaml
plugins:
  - search
  - autorefs
```

要禁用所有插件：

```yaml
plugins: []
```

### hooks

Python 脚本列表，作为简易插件使用。脚本中可以定义插件事件处理函数。

```yaml
hooks:
  - my_hooks.py
```

## 其他配置

### use_directory_urls

是否使用目录式 URL。

```yaml
use_directory_urls: true
```

**默认值**：`true`

### repo_url

源代码仓库链接。

```yaml
repo_url: https://github.com/user/repo
```

### edit_uri

编辑链接的 URI 后缀。

```yaml
edit_uri: blob/main/docs/
```

### strict

严格模式，遇到警告时停止构建。

```yaml
strict: false
```

### dev_addr

开发服务器地址。

```yaml
dev_addr: 127.0.0.1:8000
```

### extra

传递给模板的额外数据。

```yaml
extra:
  version: 1.0.0
```

### extra_css

额外的 CSS 文件。

```yaml
extra_css:
  - css/custom.css
```

### extra_javascript

额外的 JavaScript 文件。

```yaml
extra_javascript:
  - js/custom.js
```

### watch

`serve` 时额外监视的目录。

```yaml
watch:
  - properdocs
```

## 验证配置

### validation

配置链接验证的严格程度。每个值可以是 `warn`、`info`、`ignore`。

```yaml
validation:
  nav:
    omitted_files: info
    not_found: warn
    absolute_links: info
  links:
    not_found: warn
    anchors: info
    absolute_links: info
    unrecognized_links: info
```

## 环境变量

可以使用 `!ENV` 标签从环境变量读取配置值。

```yaml
site_name: !ENV SITE_NAME
site_name: !ENV [SITE_NAME, '默认站点名称']
```

## 完整配置示例

```yaml
site_name: 我的项目文档
site_url: https://example.com/docs/
site_description: 项目文档
site_author: 开发团队

repo_url: https://github.com/user/repo
edit_uri: blob/main/docs/

theme:
  name: material
  language: zh
  palette:
    - scheme: default
      primary: indigo
      accent: indigo

nav:
  - 首页: index.md
  - 指南:
    - 入门: guide/getting-started.md
    - 配置: guide/configuration.md

pandoc:
  format: markdown+raw_html+raw_attribute
  to: html5
  args:
    - --wrap=none
  html_parser: html.parser

plugins:
  - search
  - autorefs

strict: false
use_directory_urls: true
```
