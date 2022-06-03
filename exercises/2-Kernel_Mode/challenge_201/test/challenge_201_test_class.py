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
        self.set_command_list(['sudo', 'insmod', self._full_challenge_bin])
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
    # Methods listed in from "basic" to "in depth" testing fidelity.
    def build_challenge_bin(self) -> None:
        """Build the challenge binary.

        1. Builds the binary
        """
        self._build_challenge_bin()

    def load_challenge_bin(self) -> None:
        """Loads the challenge binary.

        1. Builds the binary
        2. Clears the kernel message log
        3. Loads the kernel module
        """
        # Build
        self.build_challenge_bin()
        # Clear
        self._clear_kernel_log()
        # Load
        self._load_kernel_module()

    def check_for_load_msg(self, log_entries: list, level: str = '') -> None:
        """Loads the binary and verifies log_entries are in the kernel log.

        1. Builds the binary
        2. Clears the kernel message log
        3. Loads the kernel module
        4. Checks the kernel log for log_entries

        Input validation is handled by self._check_kernel_log().

        Args:
            log_entries: A non-empty list of log_entries, as strings, to verify are in the kernel
                log.  NOTE: If you felt compelled to call this method with an empty list, just
                use self.load_challenge_bin() instead.
            level: Optional; A log level to restrict the entries viewed.  This method will ignore
                an empty level value.  Supported log levels:
                    emerg - system is unusable
                    alert - action must be taken immediately
                    crit - critical conditions
                    err - error conditions
                    warn - warning conditions
                    notice - normal but significant condition
                    info - informational
                    debug - debug-level messages

        Raises:
            None.  Calls self.fail() or self._add_test_failure(), as appropriate, instead.
        """
        # Load
        self.load_challenge_bin()
        # Check
        self.check_for_load_msg(log_entries=log_entries, level=level)

    def present_test_failures(self) -> None:
        """Present test failures."""
        self._present_test_failures()

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

    def _check_kernel_log(self, log_entries: list, level: str = '') -> None:
        """Verify log_entries can be found in the kernel log.

        Uses dmesg -k to view the kernel messages.  If level is specified, passed to dmesg's
        --level parameter to restrict the kernel messages by log level.

        Args:
            log_entries: A non-empty list of strings to ensure are found in the kernel log.
            level: Optional; A log level to restrict the entries viewed.  This method will ignore
                an empty level value.  Supported log levels:
                    emerg - system is unusable
                    alert - action must be taken immediately
                    crit - critical conditions
                    err - error conditions
                    warn - warning conditions
                    notice - normal but significant condition
                    info - informational
                    debug - debug-level messages

        Raises:
            None.  Calls self.fail() or self._add_test_failure(), as appropriate, instead.
        """
        # LOCAL VARIABLES
        cmd_list = ['sudo', 'dmesg', '-k']  # Command to execute
        command = ''                        # Human readable command
        raw_stdout = ''                     # Stdout from the command
        raw_stderr = ''                     # Stderr from the command
        # Supported log levels taken from dmesg --help
        log_levels = ['emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug']

        # INPUT VALIDATION
        # log_entries
        self._validate_list(validate_this=log_entries, param_name='log_entries', can_be_empty=False)
        for list_entry in log_entries:
            self._validate_string(list_entry, 'entry in log_entries')
        # level
        self._validate_string(level, 'level', can_be_empty=True)
        if level not in log_levels:
            self.fail(self._test_error.format(f'{level} is an unsupported log level.  '
                                              f'Choose from this list instead: {log_levels}'))

        # MASSAGE COMMAND
        if level:
            cmd_list.append(f'--level={level}')

        # FETCH ENTRIES
        (raw_stdout, raw_stderr) = self._execute_subprocess_cmd(cmd_list=cmd_list)
        if raw_stderr:
            command = ' '.join(self._cmd_list)
            self.fail(self._test_error.format(f'Failed to execute {command} with {raw_stderr}'))
        for log_entry in log_entries:
            if log_entry not in raw_stdout:
                self._add_test_failure(f'Unable to locate {log_entry} in {raw_stdout}')

    def _clear_kernel_log(self) -> None:
        """Clear the kernel ring buffer."""
        # LOCAL VARIABLES
        cmd_list = ['sudo', 'dmesg', '--clear']  # Command to clear the buffer
        command = ' '.join(self._cmd_list)       # Human readable command

        # CLEAR IT
        (raw_stdout, raw_stderr) = self._execute_subprocess_cmd(cmd_list=cmd_list)
        if raw_stderr:
            self.fail(self._test_error.format(f'Failed to execute {command} with {raw_stderr}'))

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

    def _execute_subprocess_cmd(self, cmd_list: list) -> Tuple[str, str]:
        """Wraps calls to execute_subprocess_cmd().

        Wraps calls to hobo.subprocess_automation.execute_subprocess_cmd() to translate exceptions
        into test case failures.

        Args:
            cmd_list: A list of commands to execute in subprocess, passed in as list_of_cmds.

        Returns:
            A tuple containing stdout and stderr.

        Raises:
            None.  Calls self.fail() instead.
        """
        # LOCAL VARIABLES
        command = ''     # Human readable command
        raw_stdout = ''  # Stdout from command execution
        raw_stderr = ''  # Stderr from command execution

        # INPUT VALIDATION
        self._validate_list(validate_this=cmd_list, param_name='cmd_list', can_be_empty=False)

        # EXECUTE IT
        try:
            (raw_stdout, raw_stderr) = execute_subprocess_cmd(cmd_list)
        except (RuntimeError, TypeError, ValueError) as err:
            command = ' '.join(cmd_list)
            self.fail(self._test_error.format(f'Failed to execute comamnd: {command} with '
                                              f'{str(err)}'))

        # DONE
        return tuple((raw_stdout, raw_stderr))


    def _load_kernel_module(self) -> subprocess.Popen:
        # LOCAL VARIABLES
        command = ' '.join(self._cmd_list)  # Human readable command

        # LOAD IT
        try:
            (self._raw_stdout, self._raw_stderr) = execute_subprocess_cmd(self._cmd_list)
        except (RuntimeError, TypeError, ValueError) as err:
            self.fail(self._test_error.format(f'Failed to execute comamnd: {command} with '
                                              f'{str(err)}'))
        sleep(WAIT_TIME)  # Give the module a second to load
        # TO DO: DON'T DO NOW... use a class attribute to indicate A. a kernel module has been
        #   succesfully loaded and B. it needs to be unloaded in tearDown().

    def _run_test(self) -> None:
        """Override parent's method to execute the test case and test results.

        1. Build the kernel module
        2. Clear the kernel messages
        3. Load the kernel module
        4. Check the kernel messages
        5. Unload the kernel module
        6. Validate results
        """
        # LOCAL VARIABLES
        popen_obj = None                    # Popen object
        bin_results = None                  # BinaryResults
        command = ' '.join(self._cmd_list)  # Human readable command

        # EXECUTE
        # Build
        self._build_challenge_bin()

        # Clear
        # TO DO: DON'T DO NOW... clear the kernel messages

        # Load
        try:
            popen_obj = start_subprocess_cmd(self._cmd_list)
        except (RuntimeError, TypeError, ValueError) as err:
            self.fail(self._test_error.format(f'Failed to execute comamnd: {command} with '
                                              f'{str(err)}'))
        sleep(WAIT_TIME)  # Give the module a second to load

        # Check for "Loading"
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
