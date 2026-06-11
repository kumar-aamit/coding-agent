import datetime
import pytest
from clinic_wait_times.backend.main import calculate_wait_time

def test_calculate_wait_time():
    # Fixed point in time for reproducibility
    fixed_now = datetime.datetime(2024, 1, 1, 12, 0, 0)
    # Use datetime with fixed offset not to depend on now()
    # We'll monkey‑patch datetime.datetime.now inside the function is not possible,
    # so we simulate by passing a check‑in datetime far in the past
    check_in = datetime.datetime(2024, 1, 1, 11, 30, 0)  # 30 mins ago
    wait_seconds = calculate_wait_time(check_in)
    assert wait_seconds >= 0
    # Approx 30 minutes = 1800 seconds
    assert 1800 - 30 <= wait_seconds <= 1800 + 30  # allow small variance

def test_simple(queue_fixture):
    # Simple sanity test that the fixtures work
    pass