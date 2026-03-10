import math
import re
from typing import Any, Optional


def norm(s: Any) -> str:
    if s is None:
        return ""
    t = str(s).strip().lower()
    t = t.replace("\u00a0", " ")
    t = re.sub(r"\s+", " ", t)
    t = t.replace("ё", "е")
    return t


def parse_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        if isinstance(x, float) and math.isnan(x):
            return None
        return float(x)

    s = str(x).strip()
    if not s:
        return None

    s = s.replace("\u00A0", " ").replace(" ", "")
    s = s.replace("%", "")

    if s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "")
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")

    try:
        return float(s)
    except ValueError:
        return None


def parse_discount_percent(x: Any) -> Optional[float]:
    v = parse_number(x)
    if v is None:
        return None
    if 0 < v <= 1.0:
        return v * 100.0
    return v


def ceil_int(x: float) -> int:
    """Округление вверх до целого, с защитой от 'почти целых' из-за float."""
    eps = 1e-12
    return int(math.ceil(x - eps))
