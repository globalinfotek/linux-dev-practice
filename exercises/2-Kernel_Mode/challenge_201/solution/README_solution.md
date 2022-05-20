# KERNEL MODE SOLUTION 01: Hello World LKM

## Considerations

- The requirement to include `challenge_201` in the log messages will help the test code locate the right entries.
- The format of `challenge_201: ` gives dmesg clues to help it visually format printed log messages.
- Calls to `printk()` are very common because they are usually the most basic way of tracing and debugging kernel modules.
- `prinkt()`'s format string, while largely compatible with C99, doesn’t follow the exact same specification.

## Reading Material

- [The Linux Kernel Module Programming Guide](https://tldp.org/LDP/lkmpg/2.6/html/lkmpg.html) (see: Sections 2.1-2.2)
- [Message logging with printk](https://www.kernel.org/doc/html/latest/core-api/printk-basics.html)

## Useful Commands

- `uname -r`  # Prints the kernel version of your system
- `man dmesg`  # Various ways to print or control the kernel ring buffer
- `man insmod`  # Details on how to insert a module into the Linux kernel
- `man rmmod`  # Details on how to remove a module from the Linux kernel
- `man lsmod`  # Details on how to show the status of modules in the Linux kernel
- `cat /proc/sys/kernel/printk`  # Shows the current, default, minimum and boot-time-default log levels
