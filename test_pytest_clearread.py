# -*- coding: utf-8 -*-

pytest_plugins = "pytester"
import pytest


class TestClearTerminalReporter(object):

    def setup_method(self, method):
        self.conftest = open("./pytest_clearread.py", "r")

    def test_list_of_tests_items_formatted_correctly(self, testdir):
        testdir.makepyfile("""
            import pytest
            def test_failing_function():
                assert 0

            def test_passing_function():
                assert 1 == 1
            """)
        testdir.makeconftest(self.conftest.read())
        result = testdir.runpytest('--clear', '-s', '-vvv')

        result.stdout.fnmatch_lines([
            "*- test_list_of_tests_items_formatted_correctly.py::test_failing_function  -*",
            "test_list_of_tests_items_formatted_correctly.py::test_failing_function FAILED*",
            "*- test_list_of_tests_items_formatted_correctly.py::test_passing_function  -*",
            "test_list_of_tests_items_formatted_correctly.py::test_passing_function PASSED*"
        ])
