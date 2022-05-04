/*
 * Filename: 101_source.c
 * Brief: All exercise code for User Mode challenge 101 goes here.
 * Details:
 *     - Define the contents of initSigHandlers()
 *     - Catch all possible signals
 *     - Print "Ignoring signal: X" to stderr when a signal is caught
 *     - Feel free to define your "signal handling function" in this source file
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
    // Prepare stdout
    setvbuf(stdout, NULL, _IONBF, 0);  // Make stdout unbuffered
    setvbuf(stderr, NULL, _IONBF, 0);  // Make stderr unbuffered

    // Initialize Signal Handlers
    initSigHandlers();

    // Wait
    printf("Waiting for a signal...");
    while(1)
    {
        sleep(NAP_TIME);
        printf(".");
    }
    printf("Done\n");
    return 0;
}


/*
 * Function: ignore
 * Description: Prints the ignored signal number to stderr
 *
 * signalNo: Incoming signal value
 */
void ignore(int signalNo, siginfo_t *info, void *context)
{
    fprintf(stderr, "Ignoring signal: %d\n", signalNo);
}


void initSigHandlers(void)
{
    // LOCAL VARIABLES
    int signum = 0;                   // Signam number
    struct sigaction newAct = { 0 };  // In parameter to sigaction()
    int errnum = 0;                   // Save errno

    // SETUP
    newAct.sa_flags = SA_SIGINFO;  // Use newAct.sa_sigaction instead of newAct.sa_handler
    newAct.sa_sigaction = &ignore;  // Invoke ignore() for each handled signal

    // INIT
    for (signum = 1; signum < SIGRTMAX + 1; signum++)
    {
        // SIGKILL and SIGSTOP can't be "handled" (see: man signal)
        // 32 and 33 don't exist (see: kill -l)
        if (signum != SIGKILL && signum != SIGSTOP && signum != 32 && signum != 33)
        {
            if (-1 == sigaction(signum, &newAct, NULL))
            {
                errnum = errno;
                fprintf(stderr, "sigaction(%d, sigaction *, NULL) failed with %s (%d)\n",
                        signum, strerror(errnum), errnum);
            }
        }
    }

    // DONE
    return;
}
