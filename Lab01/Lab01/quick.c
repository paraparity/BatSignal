#include "quick.h"

int32_t choose_pivot(int32_t* buffer, int32_t low, int32_t high)
{
	return low;
}

void swap(int32_t* buffer, int32_t left, int32_t right)
{
	int32_t temp = buffer[right];
	buffer[right] = buffer[left];
	buffer[left] = temp;
}

int32_t partition(int32_t* buffer, int32_t low, int32_t high)
{
	int32_t pivotIndex = choose_pivot(buffer, low, high);
	int32_t pivotValue = buffer[pivotIndex];

	swap(buffer, pivotIndex, high);
	int32_t swapIndex = low;

	for (int32_t index = low;
	     index < high;
	     ++index)
	{
		if (buffer[index] <= pivotValue)
		{
			swap(buffer, index, swapIndex);
			++swapIndex;
		}
	}

	swap(buffer, swapIndex, high);
	return swapIndex;
}

void quick_sort_helper(int32_t* buffer, int32_t low, int32_t high)
{
	if (low < high)
	{
		int32_t index = partition(buffer, low, high);
		quick_sort_helper(buffer, low, index - 1);
		quick_sort_helper(buffer, index + 1, high);
	}
}

void quick_sort(int32_t* buffer, int32_t length)
{
	quick_sort_helper(buffer, 0, length);
}
