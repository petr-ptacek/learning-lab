tree = {
    "name": "src",
    "children": [
        {
            "name": "app",
            "children": [
                {"name": "main.py", "children": []},
                {"name": "utils.py", "children": []},
            ],
        },
        {"name": "README.md", "children": []},
    ],
}

type Node = dict


def walk(node: Node, path=""):
    children = node.get("children", [])
    path += f"/{node['name']}" if path else f"{node['name']}"
    yield path

    for child in children:
        yield from walk(child, path)


print(list(walk(tree)))
