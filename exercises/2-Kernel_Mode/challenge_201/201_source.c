/*
 * Filename: 201_source.c
 * Brief: All exercise code for Kernel Mode challenge 201 goes here.
 * Details:
 *     - Write "the simplest kernel module"
 *     - Define init_module() to:
 *         - Print "challenge_201: Loading" to the kernel log buffer
 *         - Use the "Notice" log level
 *     - Define cleanup_module() to:
 *         - Print "challenge_201: Unloading" to the kernel log buffer
 *         - Use the "Notice" log level
 *     - Feel free to use the MODULE_NAME macro to assist with message formatting
 */
#include <linux/module.h>
#include <linux/kernel.h>

#define MODULE_NAME "challenge_201: "  // Standard method of identifying the source of log messages


/*
 * Function: init_module
 * Description: Expected default name for the kernel module "start" (initialization) function.
 *     This function is called when the module is insmoded into the kernel.
 */
int init_module(void)
{
    // PRINT OPTION 1: printk() messages are printed to the kernel log buffer, which is a ring
    //  buffer exported to userspace through /dev/kmsg.  printk() messages are printed to the
    //  kernel log buffer, which is a ring buffer exported to userspace through /dev/kmsg.
    printk(KERN_NOTICE "%s%s", MODULE_NAME, "Loading\n");
    return 0;  // A non-zero return means init_module failed; module can't be loaded. 
}


/*
 * Function: cleanup_module
 * Description: Expected default name for the kernel module "end" (cleanup) function.
 *     This function is called just before the module is rmmoded.
 */
void cleanup_module(void)
{
    // PRINT OPTION 2: linux/printk.h defines a collection of MACROS to print at certain log levels.
    pr_notice("%s%s", MODULE_NAME, "Unloading\n");
}


// Descriptive information about this module
MODULE_DESCRIPTION("Linux Dev Practice Challenge 201");
MODULE_LICENSE("GPL");  // Required
