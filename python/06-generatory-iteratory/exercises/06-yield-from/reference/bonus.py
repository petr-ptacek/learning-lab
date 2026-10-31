from collections.abc import Iterator
from typing import TypedDict


class Node(TypedDict):
    name: str
    children: list["Node"]


def walk(node: Node, parent: str = "") -> Iterator[str]:
    path = f"{parent}/{node['name']}" if parent else node["name"]
    yield path
    for child in node["children"]:
        yield from walk(child, path)


tree: Node = {"name": "src", "children": [
    {"name": "app", "children": [
        {"name": "main.py", "children": []},
        {"name": "utils.py", "children": []},
    ]},
    {"name": "README.md", "children": []},
]}

print(list(walk(tree)))
print(list(walk({"name": "x", "children": []})))
