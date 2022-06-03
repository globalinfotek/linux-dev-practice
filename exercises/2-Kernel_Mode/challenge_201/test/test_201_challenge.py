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
        """LKM compiles."""
        pass

    def test_normal_02(self):
        """LKM loads."""
        pass

    def test_normal_03(self):
        """LKM logs on init."""
        pass

    def test_normal_04(self):
        """LKM logs on cleanup."""
        pass

    def test_normal_05(self):
        """Init logged at Notice level."""
        pass

    def test_normal_06(self):
        """Cleanup logged at Notic level."""
        pass
