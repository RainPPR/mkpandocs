#!/usr/bin/env python3
"""JSON filter: 为外部链接添加 target="_blank"。"""

import json
import sys


def walk(node, func):
    """递归遍历 Pandoc JSON AST，对每个节点调用 func。"""
    if isinstance(node, dict):
        func(node)
        for v in node.values():
            walk(v, func)
    elif isinstance(node, list):
        for item in node:
            walk(item, func)


def process(doc):
    """为所有外部链接添加 target="_blank" 和 rel="noopener noreferrer"。"""

    def visitor(node):
        if node.get("t") == "Link":
            attrs = node["c"][1]  # [classes, kvpairs]
            target = node["c"][2][0]  # [url, title]
            if target.startswith("http://") or target.startswith("https://"):
                kv = attrs[1]
                has_target = any(k == "target" for k, _ in kv)
                if not has_target:
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
