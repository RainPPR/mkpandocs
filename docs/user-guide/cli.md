# 命令行

MkPandocs 提供以下命令行工具。

## 基本命令

### mkpandocs new

创建新的文档项目。

```bash
mkpandocs new [目录名]
```

在指定目录创建包含 `mkpandocs.yml` 和 `docs/index.md` 的初始项目。如果不指定目录名，则在当前目录创建。

### mkpandocs serve

启动开发服务器，支持自动重载。

```bash
mkpandocs serve [选项]
```

选项：

| 选项 | 说明 |
|------|------|
| `--dev-addr IP:PORT` | 设置服务器地址（默认 `127.0.0.1:8000`） |
| `--no-livereload` | 禁用自动重载 |
| `--dirtyreload` | 脏模式，只重新构建更改的文件 |
| `-w, --watch PATH` | 额外监视的目录 |
| `--strict` | 严格模式，警告视为错误 |

示例：

```bash
# 指定端口
mkpandocs serve --dev-addr 0.0.0.0:8080

# 脏模式
mkpandocs serve --dirtyreload
```

### mkpandocs build

构建静态站点到 `site/` 目录。

```bash
mkpandocs build [选项]
```

选项：

| 选项 | 说明 |
|------|------|
| `--site-dir DIR` | 指定输出目录（默认 `site`） |
| `--use-directory-urls` | 使用目录式 URL |
| `--no-directory-urls` | 不使用目录式 URL |
| `--strict` | 严格模式 |
| `-f, --config-file FILE` | 指定配置文件路径 |

示例：

```bash
# 指定输出目录
mkpandocs build --site-dir public

# 严格模式
mkpandocs build --strict
```

### mkpandocs gh-deploy

部署到 GitHub Pages。

```bash
mkpandocs gh-deploy [选项]
```

选项：

| 选项 | 说明 |
|------|------|
| `--remote-name NAME` | 远程仓库名（默认 `origin`） |
| `--remote-branch BRANCH` | 远程分支名（默认 `gh-pages`） |
| `--message MESSAGE` | 提交信息 |
| `--force` | 强制推送 |

### mkpandocs install-deps

安装 Pandoc 依赖。

```bash
mkpandocs install-deps
```

### mkpandocs get-deps

显示所需依赖。

```bash
mkpandocs get-deps
```

## 全局选项

| 选项 | 说明 |
|------|------|
| `-V, --version` | 显示版本号 |
| `-q, --quiet` | 静默模式 |
| `-v, --verbose` | 详细输出 |
| `--help` | 显示帮助信息 |
