import datetime
import io
import time
from unittest import mock

from freezegun import freeze_time

from ntropy import measure_time


@measure_time
def _takes_one_milisecond():
    time.sleep(0.001)


@measure(disable_gc=True)
@measure_time(disable_gc=True)
def _takes_one_milisecond_with_gc_off():
    time.sleep(0.001)


@measure_time
def _takes_one_second():
    time.sleep(1)


@measure_time
def _takes_two_seconds():
    time.sleep(2)


@measure_time
def _takes_one_mocked_hour():
    time.sleep(1)


@measure_time
def _takes_two_mocked_hours():
    time.sleep(2)


@measure_time
def _takes_one_mocked_minute():
    time.sleep(1)


@measure_time
def _takes_two_mocked_minutes():
    time.sleep(2)


@measure_time
def _takes_two_mocked_hours_two_minutes_two_seconds():
    time.sleep(7322)


@measure_time
def _takes_less_than_one_milisecond():
    print("this is pretty fast boi")


def test_func_name_in_stdout():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_one_milisecond()
        out_value = out.getvalue()

        assert len(out_value) > 0, "No stdout text found."
        assert "_takes_one_milisecond" in out_value, "Couldn't find the function name in stdout."


def test_disables_garbage_collection():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_one_milisecond_with_gc_off()
        out_value = out.getvalue()
        assert len(out_value) > 0, "No stdout text found."
        assert "Disabling" in out_value, "Couldn't disable garbage collection."
        assert "Re-enabling" in out_value, "Couldn't re-enable garbage collection."


def test_takes_one_second():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_one_second()
        out_value = out.getvalue()
        should_not_be_in_stdout = ["hours", "hour", "minutes", "minute", " seconds "]
        assert len(out_value) > 0, "No stdout text found."
        assert all(
            string not in out_value for string in should_not_be_in_stdout
        ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
        assert "1 second" in out_value, "Function took an unexpected time to run."


def test_takes_two_seconds():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_two_seconds()
        out_value = out.getvalue()
        should_not_be_in_stdout = ["hours", "hour", "minutes", "minute", " second "]

        assert len(out_value) > 0, "No stdout text found."
        assert all(
            string not in out_value for string in should_not_be_in_stdout
        ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
        assert "2 seconds" in out_value, "Function took an unexpected time to run."


def test_takes_one_minute(monkeypatch):
    with freeze_time("2000-01-01 00:00:00") as frozen_datetime:

        def mock_sleep(minutes):
            td = datetime.timedelta(minutes=minutes)
            frozen_datetime.tick(td)

        monkeypatch.setattr(time, "sleep", mock_sleep)

        with mock.patch("sys.stdout", new=io.StringIO()) as out:
            _takes_one_mocked_minute()
            out_value = out.getvalue()
            should_not_be_in_stdout = ["hour", "hours", "minutes", "second", "seconds"]

            assert len(out_value) > 0, "No stdout text found."
            assert all(
                string not in out_value for string in should_not_be_in_stdout
            ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
            assert "1 minute" in out_value, "Function took an unexpected time to run."


def test_takes_two_minutes(monkeypatch):
    with freeze_time("2000-01-01 00:00:00") as frozen_datetime:

        def mock_sleep(minutes):
            td = datetime.timedelta(minutes=minutes)
            frozen_datetime.tick(td)

        monkeypatch.setattr(time, "sleep", mock_sleep)

        with mock.patch("sys.stdout", new=io.StringIO()) as out:
            _takes_two_mocked_minutes()
            out_value = out.getvalue()
            should_not_be_in_stdout = ["hour", "hours", "minute ", "second", "seconds"]

            assert len(out_value) > 0, "No stdout text found."
            assert all(
                string not in out_value for string in should_not_be_in_stdout
            ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
            assert "2 minutes" in out_value, "Function took an unexpected time to run."


def test_takes_one_hour(monkeypatch):
    with freeze_time("2000-01-01 00:00:00") as frozen_datetime:

        def mock_sleep(hours):
            td = datetime.timedelta(hours=hours)
            frozen_datetime.tick(td)

        monkeypatch.setattr(time, "sleep", mock_sleep)

        with mock.patch("sys.stdout", new=io.StringIO()) as out:
            _takes_one_mocked_hour()
            out_value = out.getvalue()
            should_not_be_in_stdout = ["hours", "minutes", "minute", "second", "seconds"]

            assert len(out_value) > 0, "No stdout text found."
            assert all(
                string not in out_value for string in should_not_be_in_stdout
            ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
            assert "1 hour" in out_value, "Function took an unexpected time to run."


def test_takes_two_hours(monkeypatch):
    with freeze_time("2000-01-01 00:00:00") as frozen_datetime:

        def mock_sleep(hours):
            td = datetime.timedelta(hours=hours)
            frozen_datetime.tick(td)

        monkeypatch.setattr(time, "sleep", mock_sleep)

        with mock.patch("sys.stdout", new=io.StringIO()) as out:
            _takes_two_mocked_hours()
            out_value = out.getvalue()
            should_not_be_in_stdout = ["hour ", "minutes", "minute", "second", "seconds"]

            assert len(out_value) > 0, "No stdout text found."
            assert all(
                string not in out_value for string in should_not_be_in_stdout
            ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
            assert "2 hours" in out_value, "Function took an unexpected time to run."


def test_takes_two_hours_two_minutes_two_seconds(monkeypatch):
    with freeze_time("2000-01-01 00:00:00") as frozen_datetime:

        def mock_sleep(seconds):
            td = datetime.timedelta(seconds=seconds)
            frozen_datetime.tick(td)

        monkeypatch.setattr(time, "sleep", mock_sleep)

        with mock.patch("sys.stdout", new=io.StringIO()) as out:
            _takes_two_mocked_hours_two_minutes_two_seconds()
            out_value = out.getvalue()
            should_not_be_in_stdout = ["hour ", "minute ", "second "]

            assert len(out_value) > 0, "No stdout text found."
            assert all(
                string not in out_value for string in should_not_be_in_stdout
            ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}.\n Got: {out_value}"
            assert "2 hours" in out_value, "Function took an unexpected time to run."
            assert "2 minutes" in out_value, "Function took an unexpected time to run."
            assert "2 seconds" in out_value, "Function took an unexpected time to run."


def test_takes_less_than_a_milisecond():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_less_than_one_milisecond()
        out_value = out.getvalue()

        assert len(out_value) > 0, "No stdout text found."
        assert "less than one milisecond" in out_value, "Function took an unexpected time to run."
