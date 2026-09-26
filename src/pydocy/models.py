from logging import Logger, getLogger
from pathlib import Path

import yaml

logger: Logger = getLogger(__name__)


class PyBase:
    def __init__(self, doc_raw: str):

        self.doc_raw: str = doc_raw
        self.doc_parsed: dict = {}

    def parse_doc(self) -> None:

        if self.doc_raw.strip() == "":
            return

        try:
            data = yaml.safe_load(self.doc_raw)
        except yaml.YAMLError as e:
            logger.warning(f"Failed to load YAML: {self.doc_raw}\n\n Error: {e}")
            return

        if not isinstance(data, dict):
            logger.warning(f"Docstring not supported: {self.doc_raw}")
            return

        self.doc_parsed = data


class PyFunction(PyBase):
    def __init__(self, doc_raw: str, func_name: str, is_async: bool):

        super().__init__(doc_raw)

        self.func_name: str = func_name
        self.is_async: bool = is_async


class PyClass(PyBase):
    def __init__(self, doc_raw: str, class_name: str, methods: list[PyFunction]):

        super().__init__(doc_raw)

        self.class_name: str = class_name
        self.methods: list[PyFunction] = methods


class PyModule(PyBase):
    def __init__(
        self,
        doc_raw: str,
        module_name: str,
        path: Path,
        classes: list[PyClass],
        functions: list[PyFunction],
        submodules: list[PyModule],
    ):

        super().__init__(doc_raw)

        self.module_name: str = module_name
        self.path: Path = path
        self.classes: list[PyClass] = classes
        self.functions: list[PyFunction] = functions
        self.submodules: list[PyModule] = submodules
