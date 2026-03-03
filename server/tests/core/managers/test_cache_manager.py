import pytest
from datetime import datetime, timezone
from uuid import uuid4
from typing import TYPE_CHECKING
from sqlalchemy import select

from app.core.managers.cache import CacheManager
from app.models import Cache

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


uuid, uuid2, now  = str(uuid4()), str(uuid4()), str(datetime.now(timezone.utc))


@pytest.mark.asyncio
async def test_cache_put_validate(test_session: "AsyncSession"):
    cm = CacheManager.manager(db_session=test_session)
    data = {
        "test_data": uuid,
        "now": now
    }
    # PUT
    await cm.put(owner=uuid, data=data, validity=300)
    query = await test_session.execute(
        select(Cache).filter_by(owner=uuid)
    )
    ins = query.scalar_one_or_none()
    assert ins
    assert ins.data["test_data"] == uuid
    assert ins.data["now"] == now
    # valid for now
    valid1 = await CacheManager.validate(ins)
    assert valid1

    # invalidate
    ins.validity = 0
    await test_session.commit()
    query = await test_session.execute(
        select(Cache).filter_by(owner=uuid)
    )
    ins2 = query.scalar_one_or_none()
    # not valid
    valid2 = await CacheManager.validate(ins2)
    assert not valid2
    # not valid will be deleted after get
    await cm.get(uuid)
    query = await test_session.execute(
        select(Cache).filter_by(owner=uuid)
    )
    no_cache = query.scalar_one_or_none()
    assert no_cache is None

async def test_cache_get_pop(test_session: "AsyncSession"):
    cm = CacheManager.manager(db_session=test_session)
    data = {
        "test_data": uuid2,
        "now": now
    }
    await cm.put(owner=uuid2, data=data, validity=300)
    # GET
    ins = await cm.get(uuid2)
    assert ins.data["test_data"] == uuid2
    # POP
    ins2 = await cm.pop(uuid2)
    assert ins2.data["test_data"] == uuid2
    # Cache was deleted
    query = await test_session.execute(
        select(Cache).filter_by(owner=uuid2)
    )
    no_cache = query.scalar_one_or_none()
    assert no_cache is None

