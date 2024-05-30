"""
Module containing a function to add two numbers and a TestCase class to test it
"""

from django.test import TestCase


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b


class TestExample(TestCase):
    """
    Test case for the add_two_numbers function.
    """

    def test_add_two_numbers(self) -> None:
        """
        Test the add_two_numbers function.
        """
        self.assertEqual(add_two_numbers(2, 2), 4)
