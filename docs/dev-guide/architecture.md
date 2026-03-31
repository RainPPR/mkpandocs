# 架构

MkPandocs 的整体架构说明。

## 项目结构

```
mkpandocs/
├── properdocs/              # 核心包
│   ├── __main__.py         # CLI 入口
│   ├── commands/           # 命令实现
│   │   ├── build.py        # 构建命令
│   │   ├── serve.py        # 服务命令
│   │   ├── new.py          # 创建项目
│   │   └── gh_deploy.py    # GitHub Pages 部署
│   ├── config/             # 配置系统
│   │   ├── defaults.py     # 配置定义（ProperDocsConfig）
│   │   ├── config_options.py # 配置选项类型
│   │   └── base.py         # 配置基类
│   ├── structure/          # 文档结构处理
│   │   ├── pages.py        # 页面处理 + Pandoc 渲染
│   │   ├── nav.py          # 导航构建
│   │   ├── files.py        # 文件处理
│   │   └── toc.py          # 目录生成
│   ├── plugins.py          # 插件系统
│   └── theme.py            # 主题处理
├── filters/                # 示例过滤器
│   ├── link_class.lua      # Lua filter
│   └── add_target_blank.py # JSON filter
├── docs/                   # 文档源文件
├── mkpandocs.yml           # 项目配置
└── pyproject.toml          # Python 包配置
```

## 渲染流程

### 1. 配置加载

```
mkpandocs.yml → ProperDocsConfig.load_file() → 验证 → 配置对象
```

配置系统基于 `SubConfig` 嵌套机制，支持类型验证和默认值。

### 2. 文件收集

```
docs_dir → 扫描 .md 文件 → 应用 exclude_docs/draft_docs → Files 对象
```

### 3. 导航构建

```
nav 配置 → 匹配 Files → Navigation 对象
```

### 4. 页面渲染

每个页面经过以下流程：

```
read_source() → Markdown 内容 + 元数据
    ↓
render() → Pandoc 处理
    ↓
    ├── 无 json_filters: markdown → html5
    └── 有 json_filters: markdown → json → filter chain → html5
    ↓
_PandocHTMLParser.process() → 提取锚点/标题、重写链接
    ↓
HTML 内容 + TOC
```

### 5. 模板渲染

```
HTML 内容 + 主题模板 → Jinja2 渲染 → 最终 HTML 文件
```

## 配置系统

### SubConfig 嵌套

配置使用 `SubConfig` 实现嵌套结构：

```python
class PandocConfig(base.Config):
    format = c.Type(str, default='markdown')
    to = c.Type(str, default='html5')

class ProperDocsConfig(base.Config):
    pandoc = c.SubConfig(PandocConfig)
```

YAML 中：

```yaml
pandoc:
  format: markdown+raw_html+raw_attribute
  to: html5
```

### 访问方式

```python
# 嵌套配置通过属性访问
config.pandoc.format  # 'markdown+raw_html+raw_attribute'
config.pandoc.to      # 'html5'

# 扁平配置通过 dict 访问
config.get('site_name', '')
```

## JSON 过滤器管线

当 `pandoc.json_filters` 非空时，渲染使用三步管线：

1. `pypandoc.convert_text(markdown, to='json', format=format)` — Markdown → JSON AST
2. 对每个 filter 执行 `subprocess.run([python, filter], input=json)` — AST 处理
3. `pypandoc.convert_text(json_data, to='html5', format='json')` — JSON AST → HTML

过滤器通过标准 I/O 通信：`stdin` 接收 JSON，`stdout` 输出 JSON。

## 与 MkDocs 的关系

MkPandocs 基于 properdocs（MkDocs 的分支）修改而来。主要变更：

- 替换 Python-Markdown 渲染引擎为 Pandoc
- 新增 `pandoc` 嵌套配置
- 新增 `json_filters` 管线
- 移除 Python-Markdown 扩展系统
- 移除部分 MkDocs 特有的插件接口
