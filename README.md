# MkPandocs

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Build Status][GHAction-image]][GHAction-link]

MkPandocs 是一个强大的静态站点生成器，专为技术文档设计。它是 [MkDocs](https://www.mkdocs.org/) 的 Pandoc 渲染分支，基于 [properdocs](https://github.com/mkdocs/mkdocs) 修改。

与原版 MkDocs 不同，MkPandocs 使用 [Pandoc](https://pandoc.org/) 作为渲染引擎。这意味着你可以利用 Pandoc 极其丰富的 Markdown 变体支持（如 `commonmark_x`, `gfm`, `pandoc` 等）以及强大的 Lua 过滤器和 JSON 过滤器系统。

> **⚠️ 项目状态**
>
> 本项目仍在积极开发中。目前已具备核心功能，欢迎试用并反馈问题。

## 核心特性

- **Pandoc 驱动**：支持几乎所有 Pandoc 的 Markdown 扩展。
- **强大的过滤器**：支持 Lua 过滤器和 Python (JSON) 过滤器，轻松扩展文档转换逻辑。
- **主题兼容**：继承了 MkDocs 的主题生态，特别是对 `mkdocs-material` 的良好支持。
- **安装便捷**：内置 `install-deps` 命令，自动安装管理 Pandoc 二进制文件。

## 快速开始

推荐使用 [uv](https://github.com/astral-sh/uv) 进行安装和管理：

```bash
# 安装 mkpandocs
uv tool install mkpandocs

# 安装 Pandoc 依赖
mkpandocs install-deps

# 创建新项目
mkpandocs new my-docs
cd my-docs

# 预览文档
mkpandocs serve
```

## 配置示例 (`mkpandocs.yml`)

```yaml
site_name: 我的文档
theme:
  name: material

pandoc:
  format: commonmark_x  # 使用更强大的 Markdown 变体
  args:
    - --wrap=none
  lua_filters:
    - filters/my-filter.lua
```

## 文档

完整的技术文档、使用方法和配置说明请访问：

**[rainppr.github.io/mkpandocs](https://rainppr.github.io/mkpandocs/)**

## 贡献指南

欢迎参与贡献！

### 开发环境

```bash
git clone https://github.com/RainPPR/mkpandocs.git
cd mkpandocs
uv sync --group dev
uv run mkpandocs install-deps
```

### 验证与格式化

```bash
# 运行测试
uv run python -m unittest discover properdocs/tests

# 格式化代码
uv format .
```

## 致谢

MkPandocs 基于 [MkDocs](https://www.mkdocs.org/) 项目开发，感谢 MkDocs 团队和 Tom Christie 等贡献者的出色工作。

## 许可证

MkPandocs 基于 [BSD-2-Clause 许可证](LICENSE) 发布。

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/mkpandocs.svg
[pypi-v-link]: https://pypi.org/project/mkpandocs/
[GHAction-image]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml/badge.svg
[GHAction-link]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml
