# 部署

MkPandocs 构建完全静态的 HTML 站点，可以部署到任何支持静态文件的服务。

## 构建

```bash
mkpandocs build
```

生成的文件位于 `site/` 目录。

## 部署到 GitHub Pages

### 自动部署

```bash
mkpandocs gh-deploy
```

这会自动将 `site/` 目录推送到 `gh-pages` 分支。

### 手动部署

```bash
mkpandocs build
git checkout gh-pages
cp -r site/* .
git add .
git commit -m "Update docs"
git push origin gh-pages
```

### GitHub Actions 自动部署

在仓库中创建 `.github/workflows/docs.yml`：

```yaml
name: Deploy Docs
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install mkpandocs
      - run: mkpandocs install-deps
      - run: mkpandocs build --strict
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## 部署到 Netlify

1. 在 Netlify 中连接你的 GitHub 仓库
2. 设置构建命令：`pip install mkpandocs && mkpandocs install-deps && mkpandocs build`
3. 设置发布目录：`site`

## 部署到 Vercel

1. 在 Vercel 中导入你的 GitHub 仓库
2. 设置构建命令：`pip install mkpandocs && mkpandocs install-deps && mkpandocs build`
3. 设置输出目录：`site`

## 部署到 Cloudflare Pages

1. 在 Cloudflare Pages 中连接你的 GitHub 仓库
2. 设置构建命令：`mkpandocs build`
3. 设置构建输出目录：`site`

## 部署到自托管服务器

构建后的 `site/` 目录是纯静态文件，可以直接用任何 Web 服务器托管：

```bash
# 使用 Python 简单服务器
cd site && python -m http.server 8080

# 使用 nginx
cp -r site/* /var/www/html/
```
