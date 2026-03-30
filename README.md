# MkPandocs

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Build Status][GHAction-image]][GHAction-link]

MkPandocs 是一个静态站点生成器，专为项目文档设计。它基于 [MkDocs](https://www.mkdocs.org/) 的核心架构，但使用 [Pandoc](https://pandoc.org/) 作为 Markdown 渲染引擎，提供了更强大的 Markdown 处理能力和更好的格式兼容性。

## 主要特性

- **Pandoc 渲染引擎**：使用 Pandoc 替代 Python-Markdown，支持更广泛的 Markdown 扩展语法
- **YAML 配置**：通过 `mkpandocs.yml` 文件定义文档结构、主题和插件设置
- **插件系统**：支持通过插件扩展功能
- **主题支持**：支持第三方主题，提供灵活的外观定制
- **静态输出**：生成适合标准 Web 服务器部署的静态 HTML

## 与 MkDocs 的区别

| 特性 | MkDocs | MkPandocs |
|------|--------|-----------|
| 渲染引擎 | Python-Markdown | Pandoc |
| 配置文件 | `mkdocs.yml` | `mkpandocs.yml` |
| 扩展语法 | Markdown 扩展 | Pandoc 扩展/Lua 过滤器 |
| 数学公式 | 需要扩展 | 原生支持 |
| 代码高亮 | 需要扩展 | 内置支持 |

## 安装

### 使用 uv（推荐）

```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建新项目
mkdir my-docs && cd my-docs
uv init

# 添加 MkPandocs 依赖
uv add mkpandocs

# 安装 Pandoc 依赖
uv run mkpandocs install-deps
```

### 从 PyPI 安装

```bash
pip install mkpandocs
mkpandocs install-deps
```

### 从源码安装

```bash
git clone https://github.com/RainPPR/mkpandocs.git
cd mkpandocs
uv sync
uv run mkpandocs install-deps
```

## 快速开始

### 1. 创建新项目

```bash
mkpandocs new my-docs
cd my-docs
```

这将创建以下目录结构：

```
my-docs/
├── mkpandocs.yml    # 配置文件
└── docs/
    └── index.md     # 文档首页
```

### 2. 编写文档

编辑 `docs/index.md`：

```markdown
# 欢迎使用 MkPandocs

这是一个示例文档。

## 功能特性

- 支持 Pandoc 渲染
- 支持 LaTeX 数学公式：$E = mc^2$
- 支持代码高亮
```

### 3. 预览文档

```bash
mkpandocs serve
```

访问 http://127.0.0.1:8000 查看文档。

### 4. 构建静态站点

```bash
mkpandocs build
```

生成的静态文件位于 `site/` 目录。

## 配置说明

### 基本配置

`mkpandocs.yml` 示例：

```yaml
site_name: 我的文档
site_description: 项目文档
site_author: 作者名称

# 文档导航
nav:
  - 首页: index.md
  - 指南:
    - 快速开始: guide/getting-started.md
    - 配置指南: guide/configuration.md
  - API 文档: api/reference.md

# 主题设置
theme: mkdocs

# Pandoc 设置
pandoc_format: markdown
pandoc_to: html5
pandoc_args:
  - --wrap=none
pandoc_lua_filters:
  - filters/custom.lua

# 仓库设置
repo_url: https://github.com/user/repo
edit_uri: blob/main/docs/
```

### 高级配置

#### 自定义 Pandoc 参数

```yaml
pandoc_args:
  - --wrap=none
  - --number-sections
  - --toc

pandoc_filters:
  - pandoc-citeproc

pandoc_lua_filters:
  - filters/abstract-to-meta.lua
```

#### 数学公式支持

MkPandocs 原生支持 LaTeX 数学公式：

```markdown
行内公式：$E = mc^2$

独立公式：

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

#### 代码高亮

代码块自动高亮：

```markdown
```python
def hello():
    print("Hello, World!")
```
```

## 命令参考

### 基本命令

| 命令 | 说明 |
|------|------|
| `mkpandocs new [dir]` | 创建新项目 |
| `mkpandocs serve` | 启动开发服务器 |
| `mkpandocs build` | 构建静态站点 |
| `mkpandocs gh-deploy` | 部署到 GitHub Pages |
| `mkpandocs install-deps` | 安装 Pandoc 依赖 |
| `mkpandocs get-deps` | 显示所需依赖 |

### 服务选项

```bash
# 指定端口
mkpandocs serve --dev-addr 0.0.0.0:8080

# 禁用实时重载
mkpandocs serve --no-livereload

# 脏模式（只重新构建更改的文件）
mkpandocs serve --dirty
```

### 构建选项

```bash
# 使用目录 URL
mkpandocs build --use-directory-urls

# 指定输出目录
mkpandocs build --site-dir public

# 严格模式（遇到警告时停止）
mkpandocs build --strict
```

## 插件系统

MkPandocs 支持通过插件扩展功能。

### 内置插件

- **search**：提供搜索功能

### 使用插件

```yaml
plugins:
  - search
  - my-custom-plugin:
      option1: value1
      option2: value2
```

### 创建插件

```python
# my_plugin.py
from properdocs.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def on_page_markdown(self, markdown, **kwargs):
        # 在 Markdown 渲染前处理
        return markdown
    
    def on_page_content(self, html, **kwargs):
        # 在 HTML 渲染后处理
        return html
```

## 主题定制

### 使用内置主题

```yaml
theme: mkdocs          # MkDocs 主题
theme: readthedocs     # ReadTheDocs 主题
```

### 自定义主题

```yaml
theme:
  name: null
  custom_dir: custom_theme/
  static_templates:
    - 404.html
```

## 部署

### 部署到 GitHub Pages

```bash
# 自动部署
mkpandocs gh-deploy

# 指定分支和远程仓库
mkpandocs gh-deploy --remote-branch main --remote-name origin
```

### 部署到其他平台

构建后的 `site/` 目录可以部署到任何静态文件托管服务：

- Netlify
- Vercel
- Cloudflare Pages
- 自托管服务器

## 开发

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/RainPPR/mkpandocs.git
cd mkpandocs

# 安装依赖
uv sync --group dev

# 安装 Pandoc
uv run mkpandocs install-deps

# 运行测试
uv run python -m unittest discover -s properdocs -p "*tests.py"

# 代码检查
uv run ruff check properdocs
uv run mypy properdocs
```

### 项目结构

```
mkpandocs/
├── properdocs/              # 核心包
│   ├── __main__.py         # CLI 入口
│   ├── commands/           # 命令实现
│   ├── config/             # 配置系统
│   ├── structure/          # 文档结构
│   │   ├── pages.py        # 页面处理
│   │   ├── nav.py          # 导航构建
│   │   ├── files.py        # 文件处理
│   │   └── toc.py          # 目录生成
│   ├── plugins.py          # 插件系统
│   ├── theme.py            # 主题处理
│   └── utils/              # 工具函数
├── docs/                   # 项目文档
├── tests/                  # 测试
├── pyproject.toml          # 项目配置
└── mkpandocs.yml           # 文档配置
```

### 贡献指南

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 使用 `ruff` 进行代码检查和格式化
- 使用 `mypy` 进行类型检查
- 遵循 PEP 8 编码规范
- 所有新功能必须包含测试

## 常见问题

### Q: 如何在数学公式中使用中文？

A: 使用 `\text{}` 命令包裹中文：

```latex
$$
\text{速度} = \frac{\text{距离}}{\text{时间}}
$$
```

### Q: 如何自定义代码高亮主题？

A: 在主题配置中指定：

```yaml
theme:
  name: mkdocs
  highlightjs: true
  hljs_style: github
```

### Q: 如何处理大型文档？

A: 使用 `mkpandocs serve --dirty` 进行脏模式开发，只重新构建更改的文件。

### Q: 如何添加自定义 CSS/JS？

A: 在配置中添加：

```yaml
extra_css:
  - css/custom.css

extra_javascript:
  - js/custom.js
```

## 许可证

MkPandocs 基于 [BSD-2-Clause 许可证](LICENSE) 发布。

## 相关链接

- [官方文档](https://rainppr.github.io/mkpandocs/)
- [PyPI 页面](https://pypi.org/project/mkpandocs/)
- [GitHub 仓库](https://github.com/RainPPR/mkpandocs)
- [问题反馈](https://github.com/RainPPR/mkpandocs/issues)
- [更新日志](https://rainppr.github.io/mkpandocs/about/release-notes/)

## 致谢

MkPandocs 基于 [MkDocs](https://www.mkdocs.org/) 项目开发，感谢 MkDocs 团队的出色工作。

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/mkpandocs.svg
[pypi-v-link]: https://pypi.org/project/mkpandocs/
[GHAction-image]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml/badge.svg
[GHAction-link]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml
