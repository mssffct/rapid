import pytest
import inspect

from app.auth import auths
from app.core.module import BaseModule
from app.core.utils import modfinder


@pytest.mark.asyncio
async def test_modfinder():
    """
    Modfinder is searching in given directory for class instances
    ignoring parent classes
    """
    result = await modfinder.load_modules("auth/auths", "authenticator")
    # parents are ignored
    assert len(result) == len(auths.__all__)
    # items are classes
    assert inspect.isclass(result[0])
    # BaseModule is in item's ancestors
    assert BaseModule in result[0].mro()
    # asking for modules in unexistent path
    empty = await modfinder.load_modules("undefined", "undefined")
    assert len(empty) == 0
