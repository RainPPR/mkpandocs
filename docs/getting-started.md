# 入门教程

本教程将带你从零开始搭建一个 MkPandocs 文档站点。

## 安装

### 使用 uv（推荐）

```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 添加 MkPandocs 依赖
uv add mkpandocs

# 安装 Pandoc 依赖
uv run mkpandocs install-deps
```

### 使用 pip

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

## 创建新项目

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

## 编写第一篇文档

编辑 `docs/index.md`：

```markdown
# 我的项目文档

欢迎使用我的项目。

## 功能特性

- 支持 Pandoc 渲染
- 支持 LaTeX 数学公式：$E = mc^2$
- 支持代码高亮
```

## 本地预览

```bash
mkpandocs serve
```

访问 [http://127.0.0.1:8000](http://127.0.0.1:8000) 查看文档。开发服务器支持自动重载——当你修改文档或配置文件时，浏览器会自动刷新。

## 构建静态站点

```bash
mkpandocs build
```

生成的静态文件位于 `site/` 目录，可以直接部署到任何静态文件托管服务。

## 命令概览

| 命令 | 说明 |
|------|------|
| `mkpandocs new [dir]` | 创建新项目 |
| `mkpandocs serve` | 启动开发服务器 |
| `mkpandocs build` | 构建静态站点 |
| `mkpandocs gh-deploy` | 部署到 GitHub Pages |
| `mkpandocs install-deps` | 安装 Pandoc 依赖 |
| `mkpandocs get-deps` | 显示所需依赖 |
