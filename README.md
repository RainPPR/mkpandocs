# MkPandocs

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Build Status][GHAction-image]][GHAction-link]

MkPandocs 是一个静态站点生成器，专为项目文档设计。它是 [MkDocs](https://www.mkdocs.org/) 的 Pandoc 渲染分支，基于 [properdocs](https://github.com/mkdocs/mkdocs) 修改，使用 [Pandoc](https://pandoc.org/) 替代 Python-Markdown 作为渲染引擎。

> **⚠️ 项目状态**
>
> 本项目仍在积极开发中，功能和 API 随时可能发生变更。目前尚未完善，**不建议用于生产环境**。

## 快速开始

```bash
pip install mkpandocs
mkpandocs install-deps
mkpandocs new my-docs
cd my-docs
mkpandocs serve
```

## 文档

完整的技术文档、使用方法和配置说明请访问：

**[rainppr.github.io/mkpandocs](https://rainppr.github.io/mkpandocs/)**

## 贡献指南

欢迎参与贡献！请遵循以下流程：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发环境

```bash
git clone https://github.com/RainPPR/mkpandocs.git
cd mkpandocs
uv sync --group dev
uv run mkpandocs install-deps
```

### 代码规范

- 使用 `ruff` 进行代码检查和格式化
- 使用 `mypy` 进行类型检查
- 所有新功能必须包含测试

## 相关链接

- [官方文档](https://rainppr.github.io/mkpandocs/)
- [PyPI 页面](https://pypi.org/project/mkpandocs/)
- [GitHub 仓库](https://github.com/RainPPR/mkpandocs)
- [问题反馈](https://github.com/RainPPR/mkpandocs/issues)

## 致谢

MkPandocs 基于 [MkDocs](https://www.mkdocs.org/) 项目开发，感谢 MkDocs 团队的出色工作。

## 许可证

MkPandocs 基于 [BSD-2-Clause 许可证](LICENSE) 发布。

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/mkpandocs.svg
[pypi-v-link]: https://pypi.org/project/mkpandocs/
[GHAction-image]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml/badge.svg
[GHAction-link]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml
