/*
 * Filename: 101_source.c
 * Brief: All exercise code for User Mode challenge 101 goes here.
 * Details:
 *     - Define the contents of initSigHandlers()
 *     - Catch all possible signals
 *     - Print "Ignoring signal" to stderr when a signal is caught
 *     - Feel free to define your "signal handling function" in this source file
 *     - Ensure your "signal handling function" is async-signal-safe
 */

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define NAP_TIME (int)5  // Number of seconds to sleep


/*
 * Function: initSigHandlers
 * Description: Install "logging" signal handlers for all possible signals
 */
void initSigHandlers(void);


int main(void)
{
    // Local variables
    char waiting[] = "Waiting for a signal...";  // Waiting message
    char done[] = "Done\n";                      // Exit message

    // Prepare output
    setvbuf(stdout, NULL, _IONBF, 0);  // Make stdout unbuffered
    setvbuf(stderr, NULL, _IONBF, 0);  // Make stderr unbuffered

    // Initialize Signal Handlers
    initSigHandlers();

    // Wait
    write(STDOUT_FILENO, waiting, sizeof(waiting));
    while(1)
    {
        sleep(NAP_TIME);
        write(STDOUT_FILENO, ".", 1);
    }
    write(STDOUT_FILENO, done, sizeof(done));
    return 0;
}


////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////// FEEL FREE TO DEFINE YOUR SIGNAL HANDLING FUNCTION HERE //////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////


void initSigHandlers(void)
{
    ////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////// PUT YOUR CODE HERE //////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////
}
