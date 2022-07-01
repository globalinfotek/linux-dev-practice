/*
 * Filename: 101_example.c
 * Brief: An example solution for User Mode challenge 101.
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


/*
 * Function: ignore
 * Description: Prints the ignored signal number to stderr
 *
 * signalNo: Incoming signal value
 */
void ignore(int signalNo, siginfo_t *info, void *context)
{
    char ignore[] = "Ignoring signal";  // Ignore message
    write(STDERR_FILENO, ignore, sizeof(ignore));
}


void initSigHandlers(void)
{
    // LOCAL VARIABLES
    int signum = 0;                         // Signam number
    struct sigaction newAct = { 0 };        // In parameter to sigaction()
    char failure[] = "sigaction() failed";  // Failure message

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
                write(STDERR_FILENO, failure, sizeof(failure));
            }
        }
    }

    // DONE
    return;
}
