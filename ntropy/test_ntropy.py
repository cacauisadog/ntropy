import io
import time
from unittest import mock

from ntropy import measure


@measure
def _takes_one_milisecond():
    time.sleep(0.001)


@measure(disable_gc=True)
def _takes_one_milisecond_with_gc_off():
    time.sleep(0.001)


@measure
def _takes_one_second():
    time.sleep(1)


@measure
def _takes_two_seconds():
    time.sleep(2)


def test_func_name_in_stdout():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_one_milisecond()
        out_value = out.getvalue()

        assert len(out_value) > 0, "No stdout text found."
        assert "_takes_one_milisecond" in out_value, "Couldn't find the function name in stdout."


def test_disable_garbage_collection():
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
        should_not_be_in_stdout = ["hours", "hour", "minutes", "minute", " seconds"]
        assert len(out_value) > 0, "No stdout text found."
        assert all(
            string not in out_value for string in should_not_be_in_stdout
        ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}"
        assert "1 second" in out.getvalue(), "Function took an unexpected time to run."


def test_takes_two_seconds():
    with mock.patch("sys.stdout", new=io.StringIO()) as out:
        _takes_two_seconds()
        out_value = out.getvalue()
        should_not_be_in_stdout = ["hours", "hour", "minutes", "minute", "second "]

        assert len(out_value) > 0, "No stdout text found."
        assert all(
            string not in out_value for string in should_not_be_in_stdout
        ), f"These strings shouldn't show up in stdout: {'|'.join(should_not_be_in_stdout)}"
        assert "2 seconds" in out.getvalue(), "Function took an unexpected time to run."
