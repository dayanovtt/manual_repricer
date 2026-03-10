from enum import Enum
from typing import Any, Dict


class Mode(str, Enum):
    REPRICE = "REPRICE"


# Простейшее хранение состояния в памяти:
# user_id - {"mode": Mode}
USER_STATE: Dict[int, Dict[str, Any]] = {}


def get_state(user_id: int) -> Dict[str, Any]:
    return USER_STATE.setdefault(user_id, {"mode": Mode.REPRICE})


def set_mode(user_id: int, mode: Mode) -> None:
    st = get_state(user_id)
    st["mode"] = mode
