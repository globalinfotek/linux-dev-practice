"""Define test cases for Challenge 101.

Define test cases for User Mode challenge 101: Signal handlers.

    Typical usage example:

    cd exercises/1-User_Mode/challenge_101
    python3 -m unittest -v                 # Run all the test cases in verbose mode
    # -or-
    python3 -m unittest -v -k boundary_01  # The one test cases that should *always* pass
    # -or-
    python3 -m unittest -v -k normal_01    # If you can make this pass, you're doing well
"""

# Standard Imports
# Third Party Imports
from test.challenge_101_test_class import Challenge101Test, SignalResults
from hobo.subprocess_wrapper import execute_subprocess_cmd
# Local Imports


class Challenge101Normal(Challenge101Test):
    """Defines normal test cases."""

    def test_normal_01(self):
        """Start, SIGQUIT, then SIGKILL.

        Test class will implicitly add a SIGKILL.
        """
        self.check_signals([SignalResults(3, False)])
        self.expect_ignore()
        self.run_test()

    def test_normal_02(self):
        """Start, SIGINT, then SIGKILL.

        Explicitly added SIGKILL."""
        self.check_signals([SignalResults(2, False), SignalResults(9, True)])
        self.expect_ignore()
        self.run_test()


class Challenge101Boundary(Challenge101Test):
    """Defines boundary test cases."""

    def test_boundary_01(self):
        """One signal: Start, then SIGKILL."""
        self.check_signals([SignalResults(9, True)])
        self.verify_stderr_empty()  # No handled signals, no output
        self.run_test()

    def test_boundary_02(self):
        """11 signals: 10 handled signals, then SIGKILL."""
        # LOCAL VARIABLES
        sig_res_list = []  # List of SignalResults for this test case

        # SETUP INPUT
        # Handled signals
        for sig_num in range(20, 31):
            sig_res_list.append(SignalResults(sig_num, False))
        # Non-handled signals
        sig_res_list.append(SignalResults(9, True))

        # RUN IT
        self.check_signals(sig_res_list)
        self.expect_ignore()
        self.run_test()

    def test_boundary_03(self):
        """Smallest valid signal: SIGHUP."""
        self.check_signals([SignalResults(1, False)])
        self.expect_ignore()
        self.run_test()

    def test_boundary_04(self):
        """Largest valid signal: SIGRTMAX."""
        self.check_signals([SignalResults(64, False)])
        self.expect_ignore()
        self.run_test()


class Challenge101Special(Challenge101Test):
    """Defines special test cases."""

    def get_dyn_rel_entries(self):
        """Get the dynamic relocation entries of the challenge binary.

        Calls `objdump -R` on the challenge binary.  Fails the test case on stderr output or on
        any Exceptions raised.

        Returns:
            Raw stdout from the call to objdump, on success.

        Raises:
            None.  Calls self.fail() instead.
        """
        # LOCAL VARIABLES
        cmd_list = ['objdump', '-R', self._full_challenge_bin]  # Command to execute
        command = ' '.join(cmd_list)                            # Human readable command
        std_out = ''                                            # stdout from command
        std_err = ''                                            # stderr from command

        # PREPARE
        self._build_challenge_bin()

        # GET INFORMATION
        try:
            (std_out, std_err) = execute_subprocess_cmd(cmd_list)
        except (RuntimeError, TypeError, ValueError) as err:
            self.fail(self._test_error.format(f'Command: {command} raised '
                                              f'exception: {str(err)}'))
        else:
            if std_err:
                self.fail(self._test_error.format(f'Command: {command} produced '
                                                  f'error {std_err}'))

        # DONE
        return std_out

    def test_special_01(self):
        """Start, SIGSTOP, SIGCONT, then SIGKILL.

        SIGSTOP pauses the process.  SIGCONT wakes it back up.  SIGKILL kills it.
        """
        self.check_signals([SignalResults(19, False), SignalResults(18, False),
                            SignalResults(9, True)])
        self.expect_ignore()
        self.run_test()

    def test_special_02(self):
        """Check the dynamic relocation records for proper API call.

        Verifies that sigaction() is being called instead of signal().

        From the man page (see: man 2 signal):
            The  behavior of signal() varies across UNIX versions, and has also varied
            historically across different versions of Linux.
            Avoid its use: use sigaction(2) instead.
        """
        # LOCAL VARIABLES
        std_out = self.get_dyn_rel_entries()  # Dynamic relocation records

        # CHECK ENTRIES
        if 'signal' in std_out:
            self._add_test_failure('signal is essentially deprecated.  See `man 2 signal`')
        if 'sigaction' not in std_out:
            self._add_test_failure("You don't seem to be making the right system call yet.")

        # PRESENT FAILURES
        self._present_test_failures()

    def test_special_03(self):
        """Check the dynamic relocation records for 'bad' function calls.

        Verifies that the binary isn't using non-reentrant and/or non-async-signal-safe function
        calls.  To that end, 101_source.c was written without use of any such function calls so,
        if they exist in the compiled binary, it stands to reason the user added them if they
        exist.

        From the man page (see: man signal-safety):
            An  async-signal-safe  function is one that can be safely called from within a signal
            handler.  Many functions are not async-signal-safe.
            The kinds of issues that render a function unsafe can be quickly understood when one
            considers the implementation of the stdio library, all of whose functions are not
            async-signal-safe.
        """
        # LOCAL VARIABLES
        std_out = self.get_dyn_rel_entries()  # Dynamic relocation records
        bad_func_list = []                    # Append bad function calls here
        # List of stdio functions taken from the stdio man page: `man stdio`
        stdio_func_list = ['clearerr', 'fclose', 'fdopen', 'feof', 'ferror', 'fflush', 'fgetc',
                           'fgetpos', 'fgets', 'fileno', 'fopen', 'fprintf', 'fpurge', 'fputc',
                           'fputs', 'fread', 'freopen', 'fscanf', 'fseek', 'fsetpos', 'ftell',
                           'fwrite', 'getc', 'getchar', 'gets', 'getw', 'mktemp', 'perror',
                           'printf', 'putc', 'putchar', 'puts', 'putw', 'remove', 'rewind',
                           'scanf', 'setbuf', 'setbuffer', 'setlinebuf', 'sprintf',
                           'sscanf', 'strerror', 'sys_errlist', 'sys_nerr', 'tempnam', 'tmpfile',
                           'tmpnam', 'ungetc', 'vfprintf', 'vfscanf', 'vprintf', 'vscanf',
                           'vsprintf', 'vsscanf']
        # NOTE: The following stdio functions get a pass because they are part of 101_source.c
        #   and are necessary: setvbuf.
        bad_func_error = ('Non-async-signal-safe functions found in {}: {}.  '
                          'See `man signal-safety`.\n'
                          f'Replicate this test with `objdump -R {self._full_challenge_bin}`')

        # CHECK ENTRIES
        for stdio_func in stdio_func_list:
            if stdio_func in std_out:
                bad_func_list.append(stdio_func)
        if bad_func_list:
            self._add_test_failure(bad_func_error.format(self._challenge_bin,
                                                         ', '.join(bad_func_list)))
        if 'write' not in std_out:
            self._add_test_failure('Did you modify the original code?  Unable to locate the '
                                   'calls to write().')

        # PRESENT FAILURES
        self._present_test_failures()
