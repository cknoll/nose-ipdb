import unittest


"""
This module contains some test with errors and failures.
Every testcase contains some local variables to be able to check that the debugger awakes in the correct namespace.
"""


def test_error():
    x = 123
    y = "some string1"
    raise Exception("Enforcing an error")


def test_failure():
    x = 345
    y = "some string2"
    assert 1 == 2, "This is a failure"


def test_failure_with_print():
    x = 567
    y = "some string3"
    # This test is here to trigger issue #16
    # https://github.com/flavioamieiro/nose-ipdb/issues/16
    print("Test")
    assert 1 == 2, "This failure has a print before it"


def test_failure_with_local_variable():
    local_variable = 'foo'
    assert local_variable == 'bar', "This is a failure with a local variable in scope"


# nosetests --rednose --ipdb-failures


class TestsCases1(unittest.TestCase):

    def test_case1(self):
        # test some known results
        x = 0
        y = 0
        self.assertEqual(x, y)

    def test_case2(self):
        # failing test
        x = 0
        y = 1.23
        self.assertEqual(x, y)

    def test_case3(self):
        # test with error
        x = 1.23
        y = bad_function()
        self.assertEqual(x, y)


def bad_function():
    x = 890
    y = "some string inside bad function"
    return 1/0
