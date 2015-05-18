#ifndef __MERGE_H__
#define __MERGE_H__
#include <stdint.h>
#include <math.h>
#include <string.h>

void merge_sort(int32_t* buffer, int32_t length);

void merge(int32_t* source, int32_t* left, int32_t* right);

#endif