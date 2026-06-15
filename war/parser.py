"""Разбор сообщений «Организация: события» из Telegram."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

class WarEventKind(str, Enum):
    ATTACK_DECLARE = "attack_declare"
    DEFENSE_DECLARE = "defense_declare"
    ATTACK_WIN = "attack_win"
    DEFENSE_WIN = "defense_win"
    LOSS = "loss"


@dataclass(frozen=True)
class WarEvent:
    kind: WarEventKind
    opponent: str | None = None
    location: str | None = None
    time: str | None = None
    format: str | None = None
    conditions: str | None = None
    battle_id: int | None = None
    raw_line: str = ""


_FMT = r"(\d+[xX]\d+)"
_TIME_FMT = rf"на\s+(\d{{1,2}}:\d{{2}})[.,\s]+{_FMT}"


_PATTERNS: list[tuple[WarEventKind, re.Pattern[str]]] = [
    (
        WarEventKind.ATTACK_WIN,
        re.compile(
            r"Захватыва(?:ет|ют)\s+(.+?)\s+в\s+бою\s+#(\d+)",
            re.IGNORECASE,
        ),
    ),
    (
        WarEventKind.DEFENSE_WIN,
        re.compile(
            r"Удержива(?:ет|ют)\s+(.+?)\s+в\s+бою\s+#(\d+)",
            re.IGNORECASE,
        ),
    ),
    (
        WarEventKind.LOSS,
        re.compile(
            r"Проигрыва(?:ет|ют)\s+(?:в\s+бою\s+#(\d+)\s+за\s+)?(.+?)\.?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        WarEventKind.DEFENSE_DECLARE,
        re.compile(
            rf"(.+?)\s+забили\s+Вашей\s+организации\s+войну\s+за\s+(.+?)\s+"
            rf"{_TIME_FMT}(?:,\s*(.+?))?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        WarEventKind.ATTACK_DECLARE,
        re.compile(
            rf"Ваша\s+организация\s+забила\s+(.+?)\s+войну\s+за\s+(.+?)\s+"
            rf"{_TIME_FMT}(?:,\s*(.+?))?\s*$",
            re.IGNORECASE,
        ),
    ),
]


def normalize_tg_text(text: str) -> str:
    t = (text or "").replace("\u00a0", " ")
    # Только формат 5х5 → 5x5, не трогаем «Захватывает» и т.п.
    t = re.sub(r"(\d)[хХ](\d)", r"\1x\2", t)
    t = re.sub(r"(\d{1,2}:\d{2})\.\s*", r"\1, ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _extract_body_line(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""

    for line in reversed(lines):
        lower = line.lower()
        if any(
            kw in lower
            for kw in (
                "войну",
                "забила",
                "забили",
                "захватыва",
                "удержива",
                "проигрыва",
            )
        ):
            return line

    return lines[-1]


def parse_war_message(text: str) -> WarEvent | None:
    raw = text or ""
    normalized = normalize_tg_text(raw)
    body = _extract_body_line(normalized)
    if not body:
        return None

    for kind, pattern in _PATTERNS:
        match = pattern.search(body)
        if not match:
            continue

        if kind == WarEventKind.ATTACK_DECLARE:
            opp, loc, time_val, fmt, cond = match.groups()
            return WarEvent(
                kind=kind,
                opponent=opp.strip(),
                location=loc.strip(),
                time=time_val.strip(),
                format=fmt.strip(),
                conditions=(cond or "").strip().rstrip("."),
                raw_line=body,
            )

        if kind == WarEventKind.DEFENSE_DECLARE:
            opp, loc, time_val, fmt, cond = match.groups()
            return WarEvent(
                kind=kind,
                opponent=opp.strip(),
                location=loc.strip(),
                time=time_val.strip(),
                format=fmt.strip(),
                conditions=(cond or "").strip().rstrip("."),
                raw_line=body,
            )

        if kind in (WarEventKind.ATTACK_WIN, WarEventKind.DEFENSE_WIN):
            loc, bid = match.groups()
            return WarEvent(
                kind=kind,
                location=loc.strip(),
                battle_id=int(bid) if bid else None,
                raw_line=body,
            )

        if kind == WarEventKind.LOSS:
            bid, loc = match.groups()
            return WarEvent(
                kind=kind,
                battle_id=int(bid) if bid else None,
                location=(loc or "").strip(),
                raw_line=body,
            )

    return None


def is_war_message(text: str) -> bool:
    return parse_war_message(text) is not None
