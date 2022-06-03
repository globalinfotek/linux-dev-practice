"""Defines test framework functionality for Challenge 201.

Defines test class for Kernel Mode challenge 201: Hello World LKM.

    Typical usage example:

    from test.challenge_201_test_class import Challenge201Test

    class MyTestCases(Challenge201Test):
        def test_case_01(self):
            self.pass('My first test case!')
"""

# Standard Imports
from subprocess import Popen, TimeoutExpired
from time import sleep
from typing import Any, NamedTuple
import os
# Third Party Imports
from hobo.disk_operations import find_path_to_dir
from hobo.makefile_automation import execute_makefile_rule
from hobo.subprocess_wrapper import execute_subprocess_cmd, start_subprocess_cmd
from hobo.validation import validate_type
from tediousstart.tediousfunctest import TediousFuncTest


WAIT_TIME = 1  # Number of seconds to wait for a binary to respond to a signal


class Challenge201Test(TediousFuncTest):
    """Functional test framework for Challenge 201.

    By default, each test case should probably follow this call order:

    TO DO: DON'T DO NOW... determine order of execution
    """

    def __init__(self, *args, **kwargs) -> None:
        self._challenge_bin = '201_source.ko'  # Name of the binary to test
        self._challenge_path = None            # Absolute path to the challenge directory
        self._full_challenge_bin = None        # Absolute path to the kernel module to test
        super().__init__(*args, **kwargs)

    def validate_results(self) -> Any:
        """Overrides parent class method to validate 101 Challenge execution.

        This method was overridden because it must be.  This method will be called by
        self._run_test() once the command has exited.

        Raises:
            None.  Calls self._add_test_failure() instead.
        """
        # Verification is covered by other TEST methods

    def setUp(self) -> None:
        """Prepares Test Case.

        Automate any preparation necessary before each Test Case executes.
        """
        self._challenge_path = find_path_to_dir('challenge_201')
        self._full_challenge_bin = os.path.join(self._challenge_path, self._challenge_bin)
        self.set_command_list([self._full_challenge_bin])  # TO DO: DON'T DO NOW... validate this
        super().setUp()

    def tearDown(self) -> None:
        """Close out the test case environment.

        Verifies there isn't an errant kernel module loaded.  Warns the user if it finds one.
        """
        # LOCAL VARIABLES
        std_out = ''                  # stdout
        cmd_list = ['lsmod']          # Command to execute
        command = ' '.join(cmd_list)  # Human readable command

        # TEAR DOWN
        super().tearDown()
        # Verify the kernel module is not loaded
        # TO DO: DON'T DO NOW... mirror challenge 101 tearDown()
        # grep output for .ko
        # if found, warn the user to rmmod it

    # TEST AUTHOR METHODS
    # Methods listed in "suggested" call order

    # CLASS HELPER METHODS
    # Methods listed in alphabetical order
    def _build_challenge_bin(self) -> None:
        """Execute the makefile rule to build the binary."""
        # LOCAL VARIABLES
        makefile = os.path.join(self._challenge_path, 'Makefile')  # Makefile filename

        # BUILD
        # Clean
        self._execute_makefile_rule(makefile, 'clean')
        # Make
        self._execute_makefile_rule(makefile, 'all')

    def _execute_makefile_rule(self, makefile: str, rule: str) -> None:
        """Wraps calls to execute_makefile_rule().

        Wraps calls to hobo.makefile_automation.execute_makefile_rule() to translate exceptions
        into test case failures.

        Args:
            makefile_filename: The relative or absolute filename to the Makefile being used.
            rule: The name of the Makefile rule being verified and executed.

        Raises:
            None.  Calls self.fail() instead.
        """
        try:
            execute_makefile_rule(makefile, rule)
        except (FileNotFoundError, OSError, RuntimeError, TypeError, ValueError) as err:
            self.fail(self._test_error.format(f'Failed to execute {makefile} rule {rule} '
                                              f'with {str(err)}'))

    def _run_test(self) -> None:
        """Override parent's method to execute the test case and test results.

        1. Build the binary
        1. Execute the binary
        2. Send it signals
        3. Validate exit
        4. Validate results
        """
        # LOCAL VARIABLES
        popen_obj = None                    # Popen object
        bin_results = None                  # BinaryResults
        command = ' '.join(self._cmd_list)  # Human readable command

        # EXECUTE
        # Build
        self._build_challenge_bin()

        # Start
        try:
            popen_obj = start_subprocess_cmd(self._cmd_list)
        except (RuntimeError, TypeError, ValueError) as err:
            self.fail(self._test_error.format(f'Failed to execute comamnd: {command} with '
                                              f'{str(err)}'))
        sleep(WAIT_TIME)  # Give the binary a second to start

        # Signal
        bin_results = self._send_signals(popen_obj)

        # TEST
        # Default
        self._raw_stdout = bin_results.std_out
        self._raw_stderr = bin_results.std_err
        self._validate_default_output(bin_results.std_out, bin_results.std_err,
                                      bin_results.exit_code)

        # Other results
        self.validate_results()

    def _validate_default_output(self, std_out: str, std_err: str, exit_code: int) -> None:
        """Validate output and exit code."""
        # TEST RESULTS
        # stdout
        if self._check_stdout:
            if self._verify_stdout_empty and std_out:
                self._add_test_failure(f'Stdout was not empty: {std_out}')
            else:
                for entry in self._exp_stdout:
                    if entry not in std_out:
                        self._add_test_failure(f'Unable to locate {entry} in stdout')
        # stderr
        if self._check_stderr:
            if self._verify_stderr_empty and std_err:
                self._add_test_failure(f'Stderr was not empty: {std_err}')
            else:
                for entry in self._exp_stderr:
                    if entry not in std_err:
                        self._add_test_failure(f'Unable to locate {entry} in stderr')
        # Exit code
        if self._check_exit_code:
            if self._exp_exit_code != exit_code:
                self._add_test_failure(f'Expected exit code ({self._exp_exit_code}) '
                                       f'does not match actual exit code ({exit_code})')
