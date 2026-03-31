# 过滤器示例

## Markdown 组件类

### Admonition（提示块与折叠块）

Admonition 组件用于在文档中插入高亮提示、警告区块，以及可折叠的详情内容。本项目通过统一的 Markdown 代码块语法来实现这些扩展功能，支持在标题和正文中使用完整的 Markdown 语法（如加粗、行内代码、MathJax 公式等）。

```lua
function CodeBlock(el)
    -- 1. 检查语言是否为 md 或 markdown
    if el.classes:includes('md') or el.classes:includes('markdown') then
        
        -- 2. 获取 admonition 属性（得益于标准的 key="value" 写法，这里现在绝对稳定）
        local admonition_type = el.attributes['admonition']
        
        if admonition_type then
            
            -- 获取 title 属性
            local title_raw = el.attributes['title']
            
            -- 【细节优化】如果是 details 且没有传 title，默认给一个 "Details"
            if admonition_type == "details" and not title_raw then
                title_raw = "Details"
            else
                title_raw = title_raw or "Admonition"
            end

            -- 3. 将 title 作为 Markdown 重新解析（支持行内公式等）
            local title_doc = pandoc.read(title_raw, "markdown")
            local title_inlines = pandoc.List()
            if #title_doc.blocks > 0 and title_doc.blocks[1].content then
                title_inlines = title_doc.blocks[1].content

                
            end

            local title_doc = pandoc.read(title_raw, "markdown")
            local title_blocks = title_doc.blocks

            -- 第二个参数 {pandoc.Space()} 是块与块之间的分隔符
            -- 它会自动遍历所有 block 并提取它们的 inline 内容
            local title_inlines = pandoc.utils.blocks_to_inlines(title_blocks, {pandoc.Space()})

            -- 4. 将代码块内的文本同样作为 Markdown 重新解析
            local content_doc = pandoc.read(el.text, "markdown")
            local content_blocks = content_doc.blocks

            -- ==========================================
            -- 分支 A：处理 admonition="details" (折叠块)
            -- ==========================================
            if admonition_type == "details" then
                
                -- 构造 <summary>...</summary> 的行内元素
                local summary_inlines = pandoc.List()
                summary_inlines:insert(pandoc.RawInline("html", "<summary>"))
                summary_inlines:extend(title_inlines)
                summary_inlines:insert(pandoc.RawInline("html", "</summary>"))
                
                -- 放入纯文本段落中，防止被包进多余的 <p>
                local summary_p = pandoc.Plain(summary_inlines)

                -- 组装默认收缩的 <details> 区块
                local final_blocks = pandoc.List()
                final_blocks:insert(pandoc.RawBlock('html', '<details>'))
                final_blocks:insert(summary_p)
                final_blocks:extend(content_blocks)
                final_blocks:insert(pandoc.RawBlock('html', '</details>'))

                -- 返回包裹好的 Div
                return pandoc.Div(final_blocks, pandoc.Attr("", {"details-wrapper"}))

            -- ==========================================
            -- 分支 B：处理常规 admonition (note, warning 等)
            -- ==========================================
            else
                -- 构造 <p class="admonition-title">...</p>
                local p_start = pandoc.RawInline("html", '<p class="admonition-title">')
                local p_end   = pandoc.RawInline("html", '</p>')
                
                local p_content = pandoc.List({p_start})
                p_content:extend(title_inlines)
                p_content:insert(p_end)

                -- 必须使用 Plain (纯文本块)
                local title_p = pandoc.Plain(p_content)

                -- 组装 admonition 区块
                local final_blocks = pandoc.List({title_p})
                final_blocks:extend(content_blocks)

                -- 返回 <div class="admonition {type}">...</div>
                return pandoc.Div(final_blocks, pandoc.Attr("", {"admonition", admonition_type}))
            end
        end
    end
    
    -- 如果不是目标代码块，原样返回
    return nil
end
```

**标准语法格式** 请使用带有 `admonition` 属性的 `md` 或 `markdown` 代码块，所有属性均需包裹在 `{}` 内：

````markdown
```md {admonition="类型" title="区块标题"}
这里是内部正文内容，支持各类 Markdown 语法。
```
````

**参数说明**：

- **admonition="xxx"**（必填）：指定区块的类型。如果填入 `note`, `warning`, `tip` 等，会渲染为对应的高亮提示语块；如果填入特殊的 `details`，则会渲染为**默认收缩**的折叠详情区块。
- **title="xxx"**（可选）：区块显示的标题。如果不填，普通提示块将不生成标题，而 `details` 折叠块会默认显示 "Details"。

**使用示例 1：常规高亮提示块** 当你需要引起读者注意或做特别说明时，可以使用诸如 `warning`、`note` 等类型：

````markdown
```md {admonition="warning" title="注意：请勿除以 $0$"}
在进行上述计算时，请确保分母 **绝对不为零**，否则会引发 `ZeroDivisionError`。
```
````

**使用示例 2：详情折叠块 (Details)** 当你需要将较长、补充性的内容折叠起来，保持页面整洁时，请将类型指定为 `details`（折叠块默认处于收缩状态，用户点击后展开）：

````markdown
```md {admonition="details" title="点击查看 $E=mc^2$ 的详细推导过程"}
根据相对论，我们可以推导出：

1. 质量和能量是等价的
2. 具体的推导公式如下...
```
````

**最佳实践与避坑指南**：

- **规范书写属性**：必须确保使用键值对加引号的标准格式（如 `{admonition="note"}`），切勿将属性写在括号外，也不要混用原生类名写法（绝对不要写成 `.admonition`）。
- **标题引号转义**：如果你的 `title` 文本中本身包含双引号 `"`，请将其替换为单引号 `'` 或中文双引号 `“”`，避免破坏底层属性解析树（例如正确写法：`title="关于'测试'的说明"`）。
- **发挥 Markdown 的能力**：组件的 `title` 属性以及内部的正文区域，均已被深度接管并支持二次 Markdown 解析。请尽情在标题中使用加粗 `**`、行内代码 `` ` ``、数学公式 `$X^2$` 等复杂格式，它们都能被完美渲染。
- **保持空行隔离**：在 ` ```md ` 代码块的上方和下方，建议各保留一个**空行**，这能确保 Markdown 解析树的结构最稳固，防止由于紧贴上下文引起的渲染异常。
