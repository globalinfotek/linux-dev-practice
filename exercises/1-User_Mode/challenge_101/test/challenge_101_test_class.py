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
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousfunctest import TediousFuncTest


WAIT_TIME = 1  # Number of seconds to wait for a binary to respond to a signal


class SignalResults(NamedTuple):
    """Test author's expected results for one signal."""
    signal_num: int
    bin_exit: bool

    def validate(self) -> None:
        """Validate internal data."""
        validate_type(self.signal_num, 'signal_num', int)
        validate_type(self.bin_exit, 'bin_exit', bool)


class BinaryResults(NamedTuple):
    """Result of a binary's execution."""
    std_out: str
    std_err: str
    exit_code: int


class Challenge101Test(TediousFuncTest):

    def __init__(self, *args, **kwargs) -> None:
        self._challenge_bin = '101_challenge.bin'  # Name of the binary to test
        self._challenge_path = None                # Absolute path to the challenge directory
        self._signal_results = []                  # List of test author's expected signal results
        # Full path/filename to the binary to test
        self._full_challenge_bin = os.path.join('.', 'dist', self._challenge_bin)
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
        self.set_command_list([self._full_challenge_bin])
        self._challenge_path = find_path_to_dir('challenge_101')
        super(Challenge101Test, self).setUp()

    def tearDown(self) -> None:
        """Close out the test case environment.

        Verifies there isn't an errant binary in execution.  Warns the user if it finds one.
        """
        # LOCAL VARIABLES
        std_out = ''                               # stdout
        cmd_list = ['pidof', self._challenge_bin]  # Command to execute
        command = ' '.join(cmd_list)               # Human readable command

        # TEAR DOWN
        super(Challenge101Test, self).tearDown()
        # Look for errant binaries
        try:
            (std_out, _) = execute_subprocess_cmd(cmd_list)
        except RuntimeError as err:
                self.fail(self._test_error.format(f'Failed to execute comamnd: {command} with '
                                                  f'{str(err)}'))
        else:
            if std_out:
                self.fail(self._test_error.format(f'{self._challenge_bin} appears to still be '
                                                  f'running on PID {std_out}.  You may need to '
                                                  '`kill -SIGKILL {std_out}`'))

    # TEST AUTHOR METHODS
    # Methods listed in "suggested" call order
    def check_signals(self, signals: list) -> None:
        """Start the binary and send one or more signals.

        Signals are sent to the binary, during execution, in the order provided.  An explicit
        SIGKILL is appended to the list to ensure the binary is killed.
        """
        # INPUT VALIDATION
        self._validate_list(signals, 'signals', can_be_empty=False)
        for signal_entry in signals:
            self._validate_type(signal_entry, 'signals entry', SignalResults)
            try:
                signal_entry.validate()
            except TypeError as err:
                self.fail(self._test_error.format(err.args[0]))

        # SAVE
        self._signal_results = signals
        self._signal_results.append(SignalResults(9, True))

    # CLASS HELPER METHODS
    # Methods listed in alphabetical order
    def _build_challenge_bin(self) -> None:
        """Execute the makefile rule to build the binary."""
        # LOCAL VARIABLES
        makefile = os.path.join(self._challenge_path, 'Makefile')  # Makefile filename

        # BUILD
        # Clean
        execute_makefile_rule(makefile, 'clean')
        # Make
        execute_makefile_rule(makefile, self._challenge_bin)

    def _run_test(self) -> None:
        """Override parent's method to execute the test case and test results.

        1. Build the binary
        1. Execute the binary
        2. Send it signals
        3. Validate exit
        4. Validate results
        """
        # LOCAL VARIABLES
        popen_obj = None    # Popen object
        bin_results = None  # BinaryResults

        # EXECUTE
        # Build
        self._build_challenge_bin()

        # Start
        popen_obj = start_subprocess_cmd(self._cmd_list)
        sleep(WAIT_TIME)  # Give the binary a second to start

        # Signal
        bin_results = self._send_signals(popen_obj)

        # TEST
        # Default
        self._raw_stdout = bin_results.std_out
        self._raw_stderr = bin_results.std_err
        self._validate_default_results(bin_results.std_out, bin_results.std_err,
                                       bin_results.exit_code)

        # Other results
        self.validate_results()

    def _send_signals(self, binary: Popen) -> BinaryResults:
        """Send signals to a binary and return final default results."""
        # LOCAL VARIABLES
        std_out = ''        # stdout
        std_err = ''        # stderr
        exit_code = None    # Exit code

        # INPUT VALIDATION
        self._validate_type(binary, 'binary', Popen)

        # SEND SIGNALS
        for exp_result in self._signal_results:
            exit_code = binary.poll()
            if exit_code:
                self._add_test_failure(f'{binary.args[0]} is not running: {exit_code}')
                break
            else:
                binary.send_signal(exp_result.signal_num)

                while True:
                    try:
                        exit_code = binary.wait(WAIT_TIME)
                    except TimeoutExpired:
                        # Don't wait for 19 because it doesn't get any more CPU cycles
                        if exp_result.signal_num == 9:
                            continue
                        else:
                            break
                    else:
                        break

                # DETERMINE SIGNAL RESULTS
                # Test author expected an exit but it did not exit
                if exp_result.bin_exit and not exit_code:
                    self._add_test_failure(f'{binary.args[0]} did not exit on '
                                           f'signal {exp_result.signal_num}')
                    break
                # Test author did not expect an exit but it exited
                if not exp_result.bin_exit and exit_code:
                    self._add_test_failure(f'{binary.args[0]} prematurely exited on '
                                           f'signal {exp_result.signal_num}')
                    break
                # Test author expected an exit and it exited
                if exp_result.bin_exit and exit_code:
                    break

        # GET RESULTS
        # Get exit code
        if binary.poll():
            # Kill the process
            binary.send_signal(9)  # SIGKILL
            exit_code = binary.poll()
        # Get output
        (std_out, std_err) = binary.communicate()

        # DONE
        return BinaryResults(std_out, std_err, exit_code)


    def _validate_default_results(self, std_out: str, std_err: str, exit_code: int) -> None:
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
