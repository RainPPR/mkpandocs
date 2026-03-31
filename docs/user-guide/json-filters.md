# JSON 过滤器

MkPandocs 支持通过 `pandoc.json_filters` 配置自定义 Python 脚本来处理 Pandoc 的 JSON AST（抽象语法树），在 Markdown 到 HTML 的转换过程中进行中间处理。

## 工作流程

当配置了 `json_filters` 时，渲染流程变为三步：

1. Pandoc 将 Markdown 转换为 JSON AST
2. 依次执行 `json_filters` 中的 Python 脚本
3. Pandoc 将最终的 JSON AST 转换为目标格式（如 HTML5）

每个 JSON 过滤器通过 `stdin` 接收 JSON 字符串，处理后通过 `stdout` 输出修改后的 JSON 字符串。

## 配置方式

```yaml
pandoc:
  json_filters:
    - filters/my_filter.py
    - filters/another_filter.py
```

过滤器按列表顺序执行，前一个的输出是后一个的输入。

## Pandoc JSON AST 结构

Pandoc 的 JSON AST 包含三个顶层字段：

```json
{
  "pandoc-api-version": [1, 23, 1],
  "meta": {},
  "blocks": [...]
}
```

- `pandoc-api-version` — API 版本号
- `meta` — 文档元数据（frontmatter 中的内容）
- `blocks` — 内容块列表

### Block 类型

常见的 Block 类型：

| 类型 | 说明 | `c` 的结构 |
|------|------|-----------|
| `Header` | 标题 | `[level, [id, classes, kvpairs], [inline...]]` |
| `Para` | 段落 | `[inline...]` |
| `CodeBlock` | 代码块 | `[[id, classes, kvpairs], code]` |
| `BulletList` | 无序列表 | `[[block...], ...]` |
| `OrderedList` | 有序列表 | `[[start, style, delim], [block...]...]` |
| `BlockQuote` | 引用 | `[block...]` |
| `Table` | 表格 | 复杂结构 |
| `HorizontalRule` | 分割线 | null |

### Inline 类型

常见的 Inline 类型：

| 类型 | 说明 | `c` 的结构 |
|------|------|-----------|
| `Str` | 普通文本 | `"文本内容"` |
| `Emph` | 斜体 | `[inline...]` |
| `Strong` | 粗体 | `[inline...]` |
| `Code` | 行内代码 | `[[id, classes, kvpairs], code]` |
| `Link` | 链接 | `[inline..., [url, title]]` |
| `Image` | 图片 | `[inline..., [url, title]]` |
| `Math` | 数学公式 | `[math_type, formula]` |
| `Space` | 空格 | null |
| `SoftBreak` | 软换行 | null |

## 编写 JSON 过滤器

### 基本模板

```python
#!/usr/bin/env python3
"""JSON filter 的基本模板。"""

import json
import sys


def walk(node, func):
    """递归遍历 AST，对每个节点调用 func。"""
    if isinstance(node, dict):
        func(node)
        for v in node.values():
            walk(v, func)
    elif isinstance(node, list):
        for item in node:
            walk(item, func)


def process(doc):
    """处理文档。"""
    def visitor(node):
        # 在这里处理每个节点
        pass

    walk(doc, visitor)
    return doc


def main():
    doc = json.load(sys.stdin)
    doc = process(doc)
    json.dump(doc, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
```

### 示例：为外部链接添加 `target="_blank"`

```python
#!/usr/bin/env python3
"""为外部链接添加 target="_blank"。"""

import json
import sys


def walk(node, func):
    if isinstance(node, dict):
        func(node)
        for v in node.values():
            walk(v, func)
    elif isinstance(node, list):
        for item in node:
            walk(item, func)


def process(doc):
    def visitor(node):
        if node.get("t") == "Link":
            attrs = node["c"][1]
            target = node["c"][2][0]
            if target.startswith("http://") or target.startswith("https://"):
                kv = attrs[1]
                if not any(k == "target" for k, _ in kv):
                    kv.append(["target", "_blank"])
                    kv.append(["rel", "noopener noreferrer"])

    walk(doc, visitor)
    return doc


def main():
    doc = json.load(sys.stdin)
    doc = process(doc)
    json.dump(doc, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
```

### 示例：为所有标题添加自定义 class

```python
#!/usr/bin/env python3
"""为所有标题添加 class="heading"。"""

import json
import sys


def process(doc):
    for block in doc.get("blocks", []):
        if block.get("t") == "Header":
            attrs = block["c"][1]
            classes = attrs[1]
            if "heading" not in classes:
                classes.append("heading")
    return doc


def main():
    doc = json.load(sys.stdin)
    doc = process(doc)
    json.dump(doc, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
```

## 调试技巧

### 手动测试过滤器

使用 `pandoc` 命令手动测试：

```bash
# 将 Markdown 转为 JSON
echo "# Hello" | pandoc -t json

# 通过过滤器处理
echo "# Hello" | pandoc -t json | python filters/my_filter.py

# 查看最终输出
echo "# Hello" | pandoc -t json | python filters/my_filter.py | pandoc -f json -t html
```

### 打印调试信息

调试信息应输出到 `stderr`，不要输出到 `stdout`（会破坏 JSON）：

```python
import sys
import json

def process(doc):
    print(f"块数量: {len(doc['blocks'])}", file=sys.stderr)
    return doc

def main():
    doc = json.load(sys.stdin)
    doc = process(doc)
    json.dump(doc, sys.stdout, ensure_ascii=False)

if __name__ == "__main__":
    main()
```

## 项目中的示例

本项目包含两个示例过滤器：

- `filters/link_class.lua` — Lua 过滤器，为外部链接添加 CSS class
- `filters/add_target_blank.py` — JSON 过滤器，为外部链接添加 `target="_blank"`
