from datetime import datetime, timezone

import pytest

from voice_digest.periods import parse_bound, period_range


def test_all_has_no_start():
    start, end = period_range("all")
    assert start is None and end


def test_today_starts_at_local_midnight():
    now = datetime(2026, 9, 26, 15, 30, tzinfo=timezone.utc)
    start, _ = period_range("today", now)
    local_start = datetime.fromisoformat(start).astimezone()
    assert (local_start.hour, local_start.minute) == (0, 0)
    assert local_start.date() == now.astimezone().date()


def test_7d_covers_seven_calendar_days():
    now = datetime(2026, 9, 26, 15, 30, tzinfo=timezone.utc)
    start, _ = period_range("7d", now)
    assert (now.astimezone().date() - datetime.fromisoformat(start).astimezone().date()).days == 6


def test_unknown_period():
    with pytest.raises(ValueError):
        period_range("forever")


def test_date_bounds_are_inclusive_whole_days():
    start = datetime.fromisoformat(parse_bound("2026-09-01", is_end=False)).astimezone()
    end = datetime.fromisoformat(parse_bound("2026-09-01", is_end=True)).astimezone()
    assert (start.hour, end.hour, end.minute) == (0, 23, 59)
    assert parse_bound(None, is_end=True) is None
