# Standard Imports
from subprocess import Popen
from typing import Any, NamedTuple
import os
# Third Party Imports
from hobo.disk_operations import find_path_to_dir
from hobo.makefile_automation import execute_makefile_rule
from hobo.subprocess_wrapper import start_subprocess_cmd
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
        self.set_command_list([os.path.join('.', 'dist', self._challenge_bin)])
        self._challenge_path = find_path_to_dir('challenge_101')
        super(Challenge101Test, self).setUp()

    # TEST AUTHOR METHODS
    # Methods listed in "suggested" call order
    def check_signals(self, signals: list) -> None:
        """Start the binary and send a signal."""
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

    # CLASS HELPER METHODS
    # Methods listed in alphabetical order
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
        execute_makefile_rule(os.path.join(self._challenge_path, 'Makefile'), self._challenge_bin)

        # Start
        popen_obj = start_subprocess_cmd(self._cmd_list)

        # Signal
        bin_results = self._send_signals(popen_obj)

        # TEST
        # Default
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
                        if exp_result.signal_num in [9, 19]:
                            continue
                        else:
                            break
                    else:
                        break

                print(f'binary.poll() returned {exit_code}')  # DEBUGGING
                if exp_result.bin_exit and not exit_code:
                    self._add_test_failure(f'{binary.args[0]} did not exit on '
                                           f'signal {exp_result.signal_num}')
                    break
                if not exp_result.bin_exit and exit_code:
                    self._add_test_failure(f'{binary.args[0]} prematurely exited on '
                                           f'signal {exp_result.signal_num}')
                    break

        # GET RESULTS
        # Get exit code
        if not exit_code:
            # Kill the process
            binary.send_signal(19)  # SIGSTOP
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
