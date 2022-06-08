"""Define test cases for Challenge 201.

Define test cases for Kernel Mode challenge 201: Hello World LKM.

    Typical usage example:

    cd exercises/2-Kernel_Mode/challenge_201
    python3 -m unittest -v                 # Run all the test cases in verbose mode
    # -or-
    python3 -m unittest -v -k boundary_01  # The one test cases that should *always* pass
    # -or-
    python3 -m unittest -v -k normal_01    # If you can make this pass, you're doing well

Be sure to run the test cases with elevated privileges.
"""

# Standard Imports
# Third Party Imports
from test.challenge_201_test_class import Challenge201Test
# Local Imports


class Challenge201Normal(Challenge201Test):
    """Defines normal test cases."""

    def test_normal_01(self):
        """LKM compiles."""
        self.build_challenge_bin()
        self.present_test_failures()

    def test_normal_02(self):
        """LKM loads."""
        self.load_challenge_bin()
        self.present_test_failures()

    def test_normal_03(self):
        """LKM logs on init."""
        self.check_for_load_msgs(['challenge_201: Loading'])
        self.present_test_failures()

    def test_normal_04(self):
        """LKM logs on cleanup."""
        self.check_for_unload_msgs(['challenge_201: Loading', 'challenge_201: Unloading'])
        self.present_test_failures()

    def test_normal_05(self):
        """Init logged at Notice level."""
        self.check_for_load_msgs(['challenge_201: Loading'], level='notice')
        self.present_test_failures()

    def test_normal_06(self):
        """Cleanup logged at Notice level."""
        self.check_for_unload_msgs(['challenge_201: Loading', 'challenge_201: Unloading'],
                                   level='notice')
        self.present_test_failures()
