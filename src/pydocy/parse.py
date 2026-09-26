from pydocy.models import PyModule


def parse(modules: list[PyModule]):

    for module in modules:
        _parse(module)


def _parse(module: PyModule):

    for py_class in module.classes:
        py_class.parse_doc()

    for py_func in module.functions:
        py_func.parse_doc()

    for submod in module.submodules:
        _parse(submod)
