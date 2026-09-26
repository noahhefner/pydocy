import ast
from pathlib import Path

from pydocy.models import PyModule, PyClass, PyFunction


def walk_source(path: Path) -> list[PyModule]:

    return _walk_source(path, [])

def _walk_source(path, modules: list[PyModule]):

    if path.is_file() and path.name.endswith(".py"):
        modules.append(_parse_module(path))

    elif path.is_dir():
        for child_path in path.iterdir():
            if child_path.is_dir():
                return _walk_source(child_path, modules)

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
