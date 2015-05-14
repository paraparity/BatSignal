// Program:			
// Date Created:	11.05.2015
// Last Updated:	11.05.2015
// Authors:		Bryan Young, Joe Moraal, Zach Thornton		
// Description:		Prompts the user for a number of random numbers to generate, 
//			then performs sorting operations on that data (merge, quick, radix)

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

#include "merge.h"
#include "radix.h"
#include "quick.h"

void signal_handler(int sig) {
	printf("\b\bExiting...\n");
	exit(0);
}

int main(int argc, char** argv) {
	(void)signal(SIGINT, signal_handler);

	// Prompt user for number of items to generate
	// Write the random numbers to file
	// Prompt the user for the method of sort they want to use
	// Sort the file

	int32_t count;
	int32_t min;
	int32_t max;
	int32_t method;

	int32_t* numbers;

	FILE* unsorted;
	FILE* sorted;

	char buffer[1024];
	int32_t buffer_length = 1024;
	size_t bytes_read = 0;

	/* generate a seed for the random number generator */
	srand(time(NULL));

	/* open sorted.txt and unsorted.txt */
	unsorted = fopen("unsorted.txt", "w+");
	sorted = fopen("sorted.txt", "w+");

	/* ask the user for configuration values */
	printf("Random numbers to generate: ");
	scanf("%d", &count);
	printf("\nMinimum value: ");
	scanf("%d", &min);
	printf("Maximum value: ");
	scanf("%d", &max);
	printf("\nEnter 1 for merge\nEnter 2 for radix\nEnter 3 for quick\nChoose a sorting method: ");
	scanf("%d", &method);

	numbers = malloc(count * sizeof(int32_t));
	
	for (int32_t index = 0;
	     index < count;
	     ++index)
	{
		numbers[index] = rand() % (max - min + 1) + min;
		fprintf(unsorted, "%d ", numbers[index]);	
	}

	fprintf(unsorted, "\n");	
	fflush(unsorted);
	
	/* read in the numbers that were just output */
	fseek(unsorted, 0, SEEK_SET);
	bytes_read = fread(buffer, 1, buffer_length, unsorted);
	buffer[bytes_read] = '\0';
	
	/* parse the numbers from the string */
	int32_t index = 0;
	for (char* token = strtok(buffer, " ");
	     token != NULL && index < count;
	     token = strtok(NULL, " "), ++index)
	{
		numbers[index] = atoi(token);
	}

	fclose(unsorted);	

	/* sort the array */
	switch (method)
	{
	case 1: merge_sort(numbers, count); break;
	case 2: radix_sort(numbers, count); break;
	case 3: quick_sort(numbers, count); break;
	
	default: printf("Invalid sorting method specified.");
	}

	for (int32_t index = 0;
	     index < count;
	     ++index)
	{
		fprintf(sorted, "%d ", numbers[index]);
	}

	free(numbers);

	fprintf(sorted, "\n");
	fflush(sorted);
	fclose(sorted);
	
	return 0;
}
