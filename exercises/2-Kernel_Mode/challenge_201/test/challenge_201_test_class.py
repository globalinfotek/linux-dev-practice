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
from typing import Any, NamedTuple, Tuple
import os
# Third Party Imports
from hobo.disk_operations import find_path_to_dir
from hobo.makefile_automation import execute_makefile_rule
from hobo.misc import check_euid
from hobo.subprocess_wrapper import execute_subprocess_cmd, start_subprocess_cmd
from hobo.validation import validate_type
from tediousstart.tediousfunctest import TediousFuncTest


WAIT_TIME = 1  # Number of seconds to wait for a binary to respond to a signal


class Challenge201Test(TediousFuncTest):
    """Functional test framework for Challenge 201.

    By default, each test case should probably follow this call order:

    Call one, and only one, of the following methods in your test case:
        self.build_challenge_bin()
        -or-
        self.load_challenge_bin()
        -or-
        self.check_for_load_msgs()
        -or-
        self.check_for_unload_msgs()
    """

    def __init__(self, *args, **kwargs) -> None:
        self._challenge_LKM = '201_source'                 # Name of the Linux Kernel Module
        self._challenge_bin = self._challenge_LKM + '.ko'  # Name of the binary to test
        self._challenge_path = None                        # Abs path to the challenge directory
        self._full_challenge_bin = None                    # Abs path to the kernel module to test
        self._module_loaded = False                        # Indicates a module needs to be removed
        self._done = False                                 # Controls test case usage
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
        if not check_euid():
            self.fail(self._test_error.format('This test case requires elevated privileges'))
        self._challenge_path = find_path_to_dir('challenge_201')
        self._full_challenge_bin = os.path.join(self._challenge_path, self._challenge_bin)
        self.set_command_list(['sudo', 'insmod', self._full_challenge_bin])
        super().setUp()

    def tearDown(self) -> None:
        """Close out the test case environment.

        Verifies there isn't an errant kernel module loaded.  Warns the user if it finds one.
        """
        # HANDLE ERRANT MODULES
        # Did the test case load a module?
        if self._module_loaded:
            self._remove_kernel_module()
        # Verify the kernel module is not loaded
        if self._challenge_LKM in self._get_loaded_kernel_modules():
            self.fail(self._test_error.format(f'{self._full_challenge_bin} appears to still be '
                                              'loaded in the kernel.  You may need to '
                                              f'`rmmod {self._challenge_LKM}`'))

        # TEAR DOWN
        super().tearDown()

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

    def check_for_load_msgs(self, log_entries: list, level: str = '') -> None:
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
        self._check_kernel_log(log_entries=log_entries, level=level)

    def check_for_unload_msgs(self, log_entries: list, level: str = '') -> None:
        """Loads the binary, removes the binary, and verifies log_entries are in the kernel log.

        1. Builds the binary
        2. Clears the kernel message log
        3. Loads the kernel module
        4. Removes the kernel module
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
        # Remove
        self._remove_kernel_module()
        # Check
        self._check_kernel_log(log_entries=log_entries, level=level)

    def present_test_failures(self) -> None:
        """Wraps _present_test_failures() to verify it was called only once."""
        if self._done:
            self.fail(self._test_error.format('Test failures have already been presented!'))
        self._done = True  # *Now* they've been presented
        self._present_test_failures()  # Present them

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
        self._execute_makefile_rule(makefile, 'all', conditional_success=True)  # Look for the ko

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
        if level and level not in log_levels:
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

    def _execute_makefile_rule(self, makefile: str, rule: str,
                               conditional_success: bool = False) -> None:
        """Wraps calls to execute_makefile_rule().

        Wraps calls to hobo.makefile_automation.execute_makefile_rule() to translate exceptions
        into test case failures.

        Args:
            makefile_filename: The relative or absolute filename to the Makefile being used.
            rule: The name of the Makefile rule being verified and executed.
            conditional_success: Optional; Sometimes bad things happen to good makefile rules.
                (e.g., In the CDE, there's a clockskew.  On bare metal, Make can't find vmlinux.)
                If True, verify the existence of self._full_challenge_bin before declaring
                a failure.

        Raises:
            None.  Calls self.fail() instead.
        """
        # LOCAL VARIABLES
        fail = True  # Controls whether or not to call self.fail() in Exception

        # INPUT VALIDATION
        self._validate_type(conditional_success, 'conditional_success', bool)
        # The remaining arguments are validated by execute_makefile_rule()

        # EXECUTE IT
        try:
            execute_makefile_rule(makefile, rule)
        except (FileNotFoundError, OSError, RuntimeError, TypeError, ValueError) as err:
            if conditional_success and os.path.isfile(self._full_challenge_bin):
                fail = False  # Conditionally, it succeeded
            if fail:
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

    def _get_loaded_kernel_modules(self) -> str:
        """Use subprocess to get the modules in the Linux kernel.

        Executes lsmod and returns stdout as a string.  Calls self.fail() on stderr.

        Raises:
            None.  Calls self.fail() instead.

        Returns:
            stdout from the lsmod command.
        """
        # LOCAL VARIABLES
        cmd_list = ['lsmod']  # Command to execute
        raw_stdout = ''       # Command execution stdout
        raw_stderr = ''       # Command execution stderr

        # GET IT
        (raw_stdout, raw_stderr) = self._execute_subprocess_cmd(cmd_list)
        if raw_stderr:
            self.fail(self._test_error.format(f'lsmod command errored with {raw_stderr}'))

        # DONE
        return raw_stdout

    def _load_kernel_module(self) -> None:
        """Use subprocess to load the test case kernel module."""
        # LOCAL VARIABLES
        command = ' '.join(self._cmd_list)  # Human readable command

        # LOAD IT
        (self._raw_stdout, self._raw_stderr) = self._execute_subprocess_cmd(self._cmd_list)
        sleep(WAIT_TIME)  # Give the module a second to load
        self._module_loaded = True  # Informs tearDown() the module should be removed

    def _remove_kernel_module(self) -> None:
        """Use subprocess to remove the test case kernel module.

        Calls sudo rmmod on the _full_challenge_bin attribute.  Sets the _module_loaded attribute
        to false on success.
        """
        # LOCAL VARIABLES
        cmd_list = ['sudo', 'rmmod', self._full_challenge_bin]  # Remove the test case LKM
        raw_stderr = ''                                         # Command execution stderr

        # REMOVE IT
        (_, raw_stderr) = self._execute_subprocess_cmd(cmd_list)
        if not raw_stderr:
            self._module_loaded = False  # It worked

    def _run_test(self) -> None:
        """Override parent's method to execute the test case and test results.

        Calls self.check_for_unload_msgs() with implicit values.
        """
        self.check_for_unload_msgs(['challenge_201: Loading', 'challenge_201: Unloading'],
                                   level='notice')
