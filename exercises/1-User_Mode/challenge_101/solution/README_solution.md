# USER MODE SOLUTION 001: Signal Handler

## Considerations

- Not all signals can be "handled" (e.g., `SIGKILL`, `SIGSTOP`)
- Not all signal numbers are supported (e.g., 32 and 33 aren't supported in the LDP CDE)
- Default actions are fine if all you want your signal handler to do is terminate, ignore, dump, stop, continue, etc.  For this challenge, you'll need a signal handling function to print to stderr.  This has the double benefit of forcing you to use a call-back function and making it easy for the functional tests to "detect" success.

## Reading Material

- [The Linux Programming Interface](https://sciencesoftcode.files.wordpress.com/2018/12/the-linux-programming-interface-michael-kerrisk-1.pdf) (see: Chapters 20-22)
- [sigaction man page](https://man7.org/linux/man-pages/man2/sigaction.2.html)
- [signal-safety man page](https://man7.org/linux/man-pages/man7/signal-safety.7.html)
- [Details about signals](https://www.tutorialspoint.com/unix/unix-signals-traps.htm)

## Useful Commands

- `kill -l`  # Display signals supported by your system
- `man 2 signal`  # Should lead you to `sigaction()`
- `man 2 sigaction`  # Most of what you need to know
- `man signal-safety`  # Information regarding async-signal-safe functions
- `man stdio`  # List of stdio functions tested against were taken from here
