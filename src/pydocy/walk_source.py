import ast
from pathlib import Path

from pydocy.models import PyClass, PyFunction, PyModule


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
    module = PyModule(
        doc_raw=ast.get_docstring(tree) or "",
        module_name=path.name,
        path=path,
        classes=[],
        functions=[],
        submodules=[],
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_node = PyFunction(
                doc_raw=ast.get_docstring(node) or "",
                func_name=node.name,
                is_async=False,
            )
            module.functions.append(func_node)
        elif isinstance(node, ast.AsyncFunctionDef):
            func_node = PyFunction(
                doc_raw=ast.get_docstring(node) or "",
                is_async=True,
                func_name=node.name,
            )
            module.functions.append(func_node)
        elif isinstance(node, ast.ClassDef):
            class_node = PyClass(
                doc_raw=ast.get_docstring(node) or "",
                class_name=node.name,
                methods=[],
            )
            for child_node in ast.walk(node):
                if isinstance(child_node, ast.FunctionDef):
                    method_node = PyFunction(
                        doc_raw=ast.get_docstring(child_node) or "",
                        func_name=child_node.name,
                        is_async=False,
                    )
                    class_node.methods.append(method_node)
                elif isinstance(child_node, ast.AsyncFunctionDef):
                    method_node = PyFunction(
                        doc_raw=ast.get_docstring(child_node) or "",
                        func_name=child_node.name,
                        is_async=True,
                    )
                    class_node.methods.append(method_node)
            module.classes.append(class_node)
    return module
