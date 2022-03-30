/*
 * Filename: 101_source.c
 * Brief: All exercise code for User Mode challenge 101 goes here.
 * Details:
 *     - Define the contents of initSigHandlers()
 *	   - Catch all possible signals
 *	   - Print "Ignoring signal: X" to stderr when a signal is caught
 *	   - Feel free to define your "signal handling function" in this source file
 */

#include <stdio.h>
#include <unistd.h>

#define NAP_TIME (int)5  // Number of seconds to sleep


/*
 * Function: initSigHandlers
 * Description: Install "logging" signal handlers for all possible signals
 */
void initSigHandlers(void);


void main(void)
{
	// Prepare stdout
	setvbuf(stdout, NULL, _IONBF, 0);  // Make stdout unbuffered

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
}


/*
 *
 */
void initSigHandlers(void)
{
	return;
}
