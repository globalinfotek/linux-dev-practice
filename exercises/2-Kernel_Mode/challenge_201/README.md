# KERNEL MODE CHALLENGE 01: Hello World LKM

## Description

Write a "Hello Word" Linux Kernel Module (LKM).

## Details

- Edit `201_source.c` to solve this challenge.
- Define ` ` to implement your LKM.
- Verify your results (see: "Testing" section below).
- An example source file and amplifying considerations can be found in the `solution` directory.

## Testing

### Manual Testing

```
cd exercises/2-Kernel_Mode/challenge_201/  # Manual testing in the local directory is easier
make clean  # Ensure you build from scratch
make  # Watch for errors
... 201_challenge.ko  # _____ the kernel module
# From a different terminal...
# TO DO: DON'T DO NOW... verify log messages
# TO DO: DON'T DO NOW... manual cleanup/LKM unloading
```

### Automated Testing

From the challenge directory:

`python3 -m unittest` Execute all challege test cases

`python3 -m unittest -v` Execute all test cases with verbose output

`python3 -m unittest -k normal` Execute all the normal test cases

`python3 -m unittest -k normal_01` Execute normal test case 1

`python3 -m unittest -k normal_01 -v` Execute normal test case 1 with verbose output
