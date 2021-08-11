"""
.. include:: ../README.md
"""

from . import errors
from ._query import Query
from ._distributed_query import DistributedQuery


__all__ = ["Query", "DistributedQuery", "errors"]
__version__ = "2.0.4"


def _fix_pdoc():
    import os
    import queue
    from types import ModuleType
    root = os.path.dirname(__file__)
    modules = queue.Queue()
    for module in __all__:
        modules.put_nowait((module, ))

    while not modules.empty():
        module_name = modules.get_nowait()
        module = eval(".".join(module_name))
        if not isinstance(module, ModuleType):
            continue
        if "__pdoc__" not in dir(module):
            module.__pdoc__ = {}
        if "__all__" not in dir(module):
            module.__all__ = []

        for obj in module.__all__:
            obj = eval(".".join(module_name) + f".{obj}")
            if not isinstance(obj, ModuleType):
                obj.__module__ = "ai." + ".".join(module_name)

        for submodule in os.listdir(os.path.join(root, *module_name)):
            submodule_path = os.path.join(root, *module_name, submodule)
            if submodule.startswith("_"):
                continue
            if os.path.isdir(submodule_path) and "__init__.py" in os.listdir(submodule_path):
                module.__pdoc__[submodule] = submodule in module.__all__
                if submodule in module.__all__:
                    modules.put_nowait(module_name + (submodule, ))
            elif submodule.endswith(".py"):
                submodule = submodule[:-3]
                module.__pdoc__[submodule] = submodule in module.__all__

_fix_pdoc()
