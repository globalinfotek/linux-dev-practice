# USER MODE CHALLENGE 001: Signal Handler

## Description

Implement a signal handler that catches and ignores all possible signals.  Write the signal
handler so that it prints "Ignoring signal: X", where X is the signum, to stderr when invoked.

## Testing

### Manual Testing

```
cd exercises/1-User_Mode/challenge_101/  # Mnual testing in the local directory is easier
make all  # Make sure it builds
./101.bin  # Invoke the binary
kill -SIGQUIT `pidof 101.bin`  # Should result in "Ignoring signal: 3"
kill -SIGSTOP `pidof 101.bin`  # Binary should exit after "Stopped                 ./101.bin"
```

### Automated Testing

TO DO: DON'T DO NOW
