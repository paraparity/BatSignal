// Program:			
// Date Created:	11.05.2015
// Last Updated:	11.05.2015
// Authors:			Bryan Young, Joe Moraal, Zach Thornton		
// Description:		Prompts the user for a number of random numbers to generate, 
//		then performs sorting operations on that data (merge, quick, radix)
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#include "merge.h"

void signal_handler(int sig) {
	printf("\b\bExiting...\n");
	exit(0);
}

int main(int argc, char** argv) {
	(void)signal(SIGINT, signal_handler);

	return 0;
}
