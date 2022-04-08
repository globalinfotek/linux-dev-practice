from test.challenge_101_test_class import Challenge101Test, SignalResults



class Challenge101Normal(Challenge101Test):

    def test_normal_01(self):
        """Start and SIGKILL."""
        self.check_signals([SignalResults(9, True)])
        self.run_test()
