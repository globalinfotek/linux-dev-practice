"""Define test cases for Challenge 201.

Define test cases for Kernel Mode challenge 201: Hello World LKM.

    Typical usage example:

    cd exercises/2-Kernel_Mode/challenge_201
    python3 -m unittest -v                 # Run all the test cases in verbose mode
    # -or-
    python3 -m unittest -v -k boundary_01  # The one test cases that should *always* pass
    # -or-
    python3 -m unittest -v -k normal_01    # If you can make this pass, you're doing well
"""

# Standard Imports
# Third Party Imports
from test.challenge_201_test_class import Challenge201Test
# Local Imports


class Challenge201Normal(Challenge201Test):
    """Defines normal test cases."""

    def test_normal_01(self):
        """TDB."""
        pass


class Challenge201Error(Challenge201Test):
    """Defines error test cases."""

    def test_error_01(self):
        """TBD."""
        pass


class Challenge201Boundary(Challenge201Test):
    """Defines boundary test cases."""

    def test_boundary_01(self):
        """TBD."""
        pass


class Challenge201Special(Challenge201Test):
    """Defines special test cases."""

    def test_special_01(self):
        """TBD."""
        pass
