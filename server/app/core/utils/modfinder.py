import inspect
import pkgutil
import importlib
from pathlib import Path
from typing import Any


async def load_modules(path: str, instance: str) -> list[Any]:
    package_dir = Path.cwd().joinpath("app", Path(path)).resolve()
    result = []
    for _, module_name, _ in pkgutil.iter_modules([package_dir.as_posix()]):
        spec = importlib.util.spec_from_file_location(
            module_name, package_dir / module_name / f"{instance}.py"
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            found = inspect.getmembers(
                module,
                lambda member: inspect.isclass(member)
                and member.__module__ == module.__name__,
            )
            for i in found:
                result.append(i[1])
        else:
            continue
    return result
