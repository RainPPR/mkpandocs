# MkPandocs

MkPandocs 是一个静态站点生成器，专为项目文档设计。它是 [MkDocs](https://www.mkdocs.org/) 的 Pandoc 渲染分支，基于 [properdocs](https://github.com/mkdocs/mkdocs) 修改，使用 [Pandoc](https://pandoc.org/) 替代 Python-Markdown 作为渲染引擎。

> **⚠️ 项目状态**
>
> 本项目仍在积极开发中，功能和 API 随时可能发生变更。目前尚未完善，**不建议用于生产环境**。

## 与 MkDocs 的区别

| 特性 | MkDocs | MkPandocs |
|------|--------|-----------|
| 渲染引擎 | Python-Markdown | Pandoc |
| 配置文件 | `mkdocs.yml` | `mkpandocs.yml` |
| 扩展语法 | Markdown 扩展 | Pandoc 扩展 / Lua 过滤器 / JSON 过滤器 |
| 数学公式 | 需要扩展 | 原生支持 |
| 代码高亮 | 需要扩展 | 内置支持 |
| JSON 过滤器 | 不支持 | 支持自定义 Python 脚本处理 AST |

## 快速导航

- [入门教程](getting-started.md) — 安装、创建项目、预览、构建
- [配置](user-guide/configuration.md) — 所有配置项说明
- [编写文档](user-guide/writing-your-docs.md) — Markdown 语法、数学公式、代码高亮
- [命令行](user-guide/cli.md) — CLI 命令及参数
- [部署](user-guide/deploying.md) — GitHub Pages、Netlify 等
- [JSON 过滤器](user-guide/json-filters.md) — 编写自定义 AST 处理脚本
- [插件开发](dev-guide/plugins.md) — 事件钩子、插件结构
- [主题开发](dev-guide/themes.md) — 模板结构、自定义主题
- [架构](dev-guide/architecture.md) — 渲染流程、配置系统

## 贡献

欢迎参与贡献！你可以通过以下方式参与：

- [GitHub 仓库](https://github.com/RainPPR/mkpandocs) — Fork → 创建分支 → 提交 → PR
- [问题反馈](https://github.com/RainPPR/mkpandocs/issues) — 报告 Bug 或提出建议

## 许可证

本项目基于 [BSD-2-Clause 许可证](https://github.com/RainPPR/mkpandocs/blob/master/LICENSE) 发布。
