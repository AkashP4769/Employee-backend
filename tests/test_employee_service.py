# tests/test_employee_service.py

# `pytest_asyncio` provides the *async-aware* fixture decorator. Plain
# `@pytest.fixture` doesn't know how to drive an `async def` body — you
# have to use `@pytest_asyncio.fixture` whenever the fixture itself is
# async or yields an async resource.
import pytest
# Same async-flavoured SQLAlchemy imports as the previous slide.


from auth.utils import hash_password
from employees import service as employee_service
from exceptions import NotFoundException
from models.employee import Employee


# The test is now pure "act + assert" — no engine, no create_all, no
# cleanup. Pytest sees the `db_session` parameter, runs the fixture
# above, and hands the yielded session in.
async def test_get_by_id_returns_seeded_employee(db_session):
    seeded = Employee(
        name="Ada", email="ada@example.com", password_hash=hash_password("secret123")
    )
    db_session.add(seeded)

    await db_session.commit()

    await db_session.refresh(seeded)

    fetched = await employee_service.get_employee(db_session, seeded.id)

    assert fetched.id == seeded.id
    assert fetched.email == "ada@example.com"


async def test_get_by_id_raises_when_missing(db_session):
    with pytest.raises(NotFoundException) as exc_info:
        await employee_service.get_employee(db_session, 9999)

    assert "9999" in exc_info.value.detail
