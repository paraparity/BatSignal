#include <stdint.h>
#include <stdlib.h>
#include <string.h>

void merge(int32_t* buffer, int32_t* left, int32_t *right, 
		int32_t left_len, int32_t right_len) {
	int i = 0;
	int j = 0;
	int k = 0;

	while ((i < left_len) && (j < right_len)) {
		if (left[i] < right[j]) {
			buffer[k] = left[i];
			i++;
		}
		else {
			buffer[k] = right[j];
			j++;
		}
		k++;
	}

	if (i == left_len) {
		memcpy(&buffer[k], &right[j], (right_len - j) * sizeof(int32_t));
	}
	else {
		memcpy(&buffer[k], &left[i], (left_len - i) * sizeof(int32_t));
	}
}

void merge_sort(int32_t* buffer, int32_t length) {
	int* left;
	int* right;
	int split = length / 2;

	if (length > 1) {
		left = malloc(split * sizeof(buffer[0]));
		right = malloc((length - split) * sizeof(buffer[0]));
		
		memcpy(left, buffer, split * sizeof(int32_t));
		memcpy(right, &buffer[split], (length - split) * sizeof(int32_t));

		merge_sort(left, split);
		merge_sort(right, length - split);
		merge(buffer, left, right, split, length - split);

		free(left);
		free(right);
	}
}

