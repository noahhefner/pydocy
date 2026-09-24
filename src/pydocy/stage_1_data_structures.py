from dataclasses import dataclass


@dataclass
class BaseElement:
    doc_raw: str

@dataclass
class PyFunction(BaseElement):
    func_name: str

@dataclass
class PyClass(BaseElement):
    class_name: str
    methods: list[PyFunction] | None = None

@dataclass
class Module(BaseElement):
    module_name: str
    classes: list[PyClass] | None = None
    functions: list[PyFunction] | None = None
    submodules: list[Module] | None = None