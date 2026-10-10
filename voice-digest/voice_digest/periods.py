"""Turn human time periods ("today", "last 7 days") into UTC ISO ranges."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone

PERIODS = {
    "today": "Today",
    "7d": "Last 7 days",
    "30d": "Last 30 days",
    "all": "All notes",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def period_range(period: str, now: datetime | None = None) -> tuple[str | None, str]:
    """Return (start, end) as UTC ISO strings. ``start`` is None for "all".

    "Today" and the day counts use the machine's local midnight, so "today"
    means the user's calendar day rather than the UTC one.
    """
    if period not in PERIODS:
        raise ValueError(f"Unknown period {period!r}; expected one of {sorted(PERIODS)}")
    now = (now or utc_now()).astimezone()  # local time
    end = to_iso(now)
    if period == "all":
        return None, end
    local_midnight = datetime.combine(now.date(), time.min, tzinfo=now.tzinfo)
    days_back = {"today": 0, "7d": 6, "30d": 29}[period]
    return to_iso(local_midnight - timedelta(days=days_back)), end


def parse_bound(value: str | None, *, is_end: bool) -> str | None:
    """Parse a user/tool-supplied date or datetime into a UTC ISO string.

    Accepts ``YYYY-MM-DD`` (interpreted as a whole local day, so an end date is
    inclusive) or any ISO 8601 datetime. Naive datetimes are treated as local time.
    """
    if not value:
        return None
    value = value.strip()
    try:
        d = date.fromisoformat(value)
    except ValueError:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.astimezone()
        return to_iso(dt)
    local_tz = datetime.now().astimezone().tzinfo
    if is_end:
        return to_iso(datetime.combine(d + timedelta(days=1), time.min, tzinfo=local_tz) - timedelta(seconds=1))
    return to_iso(datetime.combine(d, time.min, tzinfo=local_tz))
