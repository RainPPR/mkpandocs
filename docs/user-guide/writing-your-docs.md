# 编写文档

MkPandocs 使用 Pandoc 渲染 Markdown，支持丰富的语法。

## 文件布局

文档源文件放在 `docs_dir` 目录下（默认为 `docs/`）。推荐使用 `index.md` 作为每个目录的首页。

```
docs/
├── index.md
├── guide/
│   ├── getting-started.md
│   └── configuration.md
└── api/
    └── reference.md
```

## Markdown 基础

### 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 强调

```markdown
*斜体* 或 _斜体_
**粗体** 或 __粗体__
~~删除线~~
```

### 列表

无序列表：

```markdown
- 第一项
- 第二项
- 第三项
```

有序列表：

```markdown
1. 第一步
2. 第二步
3. 第三步
```

### 链接

```markdown
[链接文字](https://example.com)
[内部链接](guide/getting-started.md)
```

### 图片

```markdown
![替代文字](img/screenshot.png)
```

## 数学公式

MkPandocs 原生支持 LaTeX 数学公式。

### 行内公式

使用 `$...$` 嵌入行内公式：

```markdown
质能方程 $E = mc^2$ 是著名的物理公式。
```

### 独立公式

使用 `$$...$$` 创建独立公式块：

```markdown
高斯积分：

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### 常用示例

分数：

$$
\frac{a}{b}
$$

求和：

$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$

## 代码块

### 行内代码

使用反引号：`code`

### 围栏代码块

```markdown
```python
def hello():
    print("Hello, World!")
```
```

支持的语法高亮语言包括：`python`、`javascript`、`java`、`c`、`cpp`、`rust`、`go`、`bash`、`yaml`、`json`、`html`、`css` 等。

Python 示例：

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

## 表格

使用标准 Markdown 表格语法：

```markdown
| 列 1 | 列 2 | 列 3 |
|------|------|------|
| 数据 | 数据 | 数据 |
```

对齐方式：

```markdown
| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| a      |  b   |      c |
```

## 引用

```markdown
> 这是一段引用文字。
>
> 引用可以包含多个段落。
```

## 分割线

```markdown
---
```

## 转义字符

使用反斜杠转义特殊字符：

```markdown
\* 不是斜体 \*
\$ 不是公式 \$
\# 不是标题 \#
```

## 内联 HTML

如果 `pandoc.format` 包含 `raw_html` 扩展，可以直接使用 HTML：

```markdown
<details>
<summary>点击展开</summary>
这里是隐藏的内容。
</details>
```

不过建议尽量使用纯 Markdown 语法，仅在必要时使用内联 HTML。
