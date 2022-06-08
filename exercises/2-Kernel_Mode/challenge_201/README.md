# KERNEL MODE CHALLENGE 01: Hello World LKM

## Description

Write a "Hello Word" Linux Kernel Module (LKM).

## Details

- Edit `201_source.c` to solve this challenge.
- Define `init_module()` and `cleanup_module()` to implement your LKM.
- Verify your results (see: "Testing" section below).
- An example source file and amplifying considerations can be found in the `solution` directory.

## Testing

### Manual Testing

#### Compile

```
cd exercises/2-Kernel_Mode/challenge_201/  # Manual testing in the local directory is easier
make clean  # Ensure you build from scratch
make  # Watch for errors
```

#### Load the Module

```
# Accomplish these steps from the local exercise directory...
sudo insmod 201_source.ko  # Insert the module in the Linux kernel
sudo lsmod | grep 201_source  # Verify your module was loaded
# Check for your "Loading" message with one (or more) of these commands
sudo dmesg -k --level=notice  # Print only the "Notice" level kernel messages
sudo dmesg | grep challenge  # Print any kernel message that contains the phrase "challenge"
sudo dmesg | tail -n 10  # Show the last 10 entries
```

#### Remove the Module

```
# Accomplish these steps from the local exercise directory...
sudo rmmod 201_source  # Remove your module from the Linux kernel
sudo lsmod | grep 201_source  # Verify your module is no longer loaded
# Check for your "Unloading" message with one (or more) of these commands
sudo dmesg -k --level=notice  # Print only the "Notice" level kernel messages
sudo dmesg | grep challenge  # Print any kernel message that contains the phrase "challenge"
sudo dmesg | tail -n 10  # Show the last 10 entries
```

### Automated Testing

From the challenge directory:

`python3 -m unittest` Execute all challege test cases

`python3 -m unittest -v` Execute all test cases with verbose output

`python3 -m unittest -k normal` Execute all the normal test cases

`python3 -m unittest -k normal_01` Execute normal test case 1

`python3 -m unittest -k normal_01 -v` Execute normal test case 1 with verbose output

NOTE: These test cases require elevated privileges.
