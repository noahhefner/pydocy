import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PyFunction:
    func_name: str
    is_async: bool
    doc_raw: str | None = None


@dataclass
class PyClass:
    class_name: str
    methods: list[PyFunction] = field(default_factory=list)
    doc_raw: str | None = None


@dataclass
class PyModule:
    module_name: str
    path: Path
    classes: list[PyClass] = field(default_factory=list)
    functions: list[PyFunction] = field(default_factory=list)
    submodules: list[PyModule] = field(default_factory=list)
    doc_raw: str | None = None


def walk_source(path: Path, modules: list[PyModule]) -> list[PyModule]:

    if path.is_file() and path.name.endswith(".py"):
        modules.append(_parse_module(path))

    elif path.is_dir():
        for child_path in path.iterdir():
            if child_path.is_dir():
                return walk_source(child_path, modules)

            elif child_path.is_file() and child_path.name.endswith(".py"):
                modules.append(_parse_module(child_path))

    return modules


def _parse_module(path: Path) -> PyModule:

    tree: ast.Module = ast.parse(path.read_text())
    module = PyModule(module_name=path.name, path=path, doc_raw=ast.get_docstring(tree))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_node = PyFunction(
                func_name=node.name, is_async=False, doc_raw=ast.get_docstring(node)
            )
            module.functions.append(func_node)
        elif isinstance(node, ast.AsyncFunctionDef):
            func_node = PyFunction(
                func_name=node.name, is_async=True, doc_raw=ast.get_docstring(node)
            )
            module.functions.append(func_node)
        elif isinstance(node, ast.ClassDef):
            class_node = PyClass(
                class_name=node.name, methods=[], doc_raw=ast.get_docstring(node)
            )
            for child_node in ast.walk(node):
                if isinstance(node, ast.FunctionDef):
                    method_node = PyFunction(
                        func_name=child_node.name,
                        is_async=False,
                        doc_raw=ast.get_docstring(child_node),
                    )
                    class_node.methods.append(method_node)
                elif isinstance(node, ast.AsyncFunctionDef):
                    method_node = PyFunction(
                        func_name=child_node.name,
                        is_async=True,
                        doc_raw=ast.get_docstring(child_node),
                    )
                    class_node.methods.append(method_node)
            module.classes.append(class_node)
    return module
