from hobo.subprocess_wrapper import execute_subprocess_cmd
from test.challenge_101_test_class import Challenge101Test, SignalResults


class Challenge101Normal(Challenge101Test):

    def test_normal_01(self):
        """Start then SIGQUIT."""
        self.check_signals([SignalResults(3, False)])
        self.expect_stderr(['Ignoring signal: 3'])
        self.run_test()

    def test_normal_02(self):
        """Start, SIGINT, then SIGKILL."""
        self.check_signals([SignalResults(2, False), SignalResults(9, True)])
        self.expect_stderr(['Ignoring signal: 2'])
        self.run_test()


class Challenge101Boundary(Challenge101Test):

    def test_boundary_01(self):
        """One signal: Start, then SIGKILL."""
        self.check_signals([SignalResults(9, True)])
        self.verify_stderr_empty()  # No handled signals, no output
        self.run_test()

    def test_boundary_02(self):
        """11 signals: 10 non-handled signals, then SIGKILL."""
        # LOCAL VARIABLES
        sig_res_list = []  # List of SignalResults for this test case
        exp_err_list = []  # List of expected stderr output
        # List of signals to send before SIGKILL
        signal_list = [num for num in range(20, 31)]

        # SETUP INPUT
        # Handled signals
        for sig_num in signal_list:
            sig_res_list.append(SignalResults(sig_num, False))
            exp_err_list.append(f'Ignoring signal: {sig_num}')
        # Non-handled signals
        sig_res_list.append(SignalResults(9, True))

        # RUN IT
        self.check_signals(sig_res_list)
        self.expect_stderr(exp_err_list)
        self.run_test()


class Challenge101Special(Challenge101Test):

    def test_special_01(self):
        """Start, SIGSTOP, SIGCONT, then SIGKILL.

        SIGSTOP pauses the process.  SIGCONT wakes it back up.  SIGKILL kills it.
        """
        self.check_signals([SignalResults(19, False), SignalResults(18, False),
                            SignalResults(9, True)])
        self.expect_stderr(['Ignoring signal: 18'])
        self.run_test()

    def test_special_02(self):
        """Check the dynamic relocation records.

        Verifies that sigaction() is being called instead of signal().

        From the man page (see: man 2 signal):
            The  behavior of signal() varies across UNIX versions, and has also varied
            historically across different versions of Linux.
            Avoid its use: use sigaction(2) instead.
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
        except RuntimeError as err:
            self.fail(self._test_error.format(str(err)))
        else:
            if std_err:
                self.fail(self._test_error.format(f'Command: {command} produced '
                                                  f'error {std_err}'))
            if 'signal' in std_out:
                self._add_test_failure(f'signal is essentially deprecated.  See `man 2 signal`')
            if 'sigaction' not in std_out:
                self._add_test_failure("You don't seem to be making the right system call yet.")

        # PRESENT FAILURES
        self._present_test_failures()
