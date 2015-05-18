#include "radix.h"
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

void radix_sort(int32_t* buffer, int32_t length)
{
	int32_t* step = malloc(length * sizeof(int32_t));
	int32_t* count = malloc(10 * sizeof(int32_t));
	int32_t max_size = buffer[0];
	int32_t place = 1; 
	
	//Finding max arr #
	for (int i = 0; i < length; i++){
		step[i] = 0;
		if (buffer[i] > max_size)
			max_size = buffer[i];
	}

	while (max_size / place > 0){
		for (int i = 0; i < 10; i++){
			count[i] = 0;
		}	
		for (int i = 0; i < length; ++i){
			count[(buffer[i] / place%10)]++;
		}	
		for (int i = 1; i < 10; i++){
			count[i] += count[i - 1];
		}
		for (int i = length - 1; i >= 0; i--){
			step[--count[buffer[i] / place % 10]] = buffer[i];
		}	
		for (int i = 0; i < length; i++){
			buffer[i] = step[i];
		}
		//Step places
		place *= 10;
	}

	free(step);
	free(count);
}
