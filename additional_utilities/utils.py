from typing import Optional, Any


def get_string_name_cargo_status(status: int) -> str:
    return {
        1: 'Заявка создана',
        2: 'В пути',
        3: 'В пункте выдачи',
        4: 'Отменен'
    }.get(status, status)


def to_int(v: Any) -> Optional[int]:
    if v is None:
        return None

    try:
        return int(v)
    except Exception:
        return None
