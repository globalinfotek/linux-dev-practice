# USER MODE CHALLENGE 01: Signal Handler

## Description

Implement a signal handler that catches and ignores all possible signals.  Write the signal
handler so that it prints "Ignoring signal" to stderr when invoked.

## Details

- Edit `101_source.c` to solve this challenge.
- Define `initSigHandlers()` to implement your signal handlers.
- Feel free to define a signal handling function to `101_source.c`.
- You should not need to change any other code in `101_source.c` (e.g., `main()`).
- Verify your results (see: "Testing" section below).
- An example source file and amplifying considerations can be found in the `solution` directory.

## Testing

### Manual Testing

```
cd exercises/1-User_Mode/challenge_101/  # Manual testing in the local directory is easier
make clean  # Ensure you build from scratch
make  # Watch for errors
./dist/101_challenge.bin  # Invoke the binary
# From a different terminal...
kill -SIGQUIT `pidof 101_challenge.bin`  # Should result in "Ignoring signal" in original terminal
kill -SIGSTOP `pidof 101_challenge.bin`  # Binary should exit after "Stopped ./101_challenge.bin" in original terminal
```

### Automated Testing

From the challenge directory:

`python3 -m unittest` Execute all challege test cases
`python3 -m unittest -v` Execute all test cases with verbose output
`python3 -m unittest -k normal` Execute all the normal test cases
`python3 -m unittest -k normal_01` Execute normal test case 1
`python3 -m unittest -k normal_01 -v` Execute normal test case 1 with verbose output
