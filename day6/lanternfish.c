#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[]) {
    int numDays = strtol(argv[2], NULL, 10);

    unsigned long population[9];
    unsigned long working[9];

    for(int i = 0; i < 9; i++) {
        population[i] = 0;
        working[i] = 0;
    }

    // Read in file to get starting population
    FILE *fptr = fopen(argv[1], "r");

    int c;
    while((c = fgetc(fptr)) != EOF) {
        c -= 48;
        if(c < 10 && c >= 0) {
            population[c]++;
        }
    }

    for(int d = 0; d < numDays; d++) {
        // Shift everyone down one (except those at 0)
        for(int i = 1; i < 9; i++) {
            working[i-1] = population[i];
        }
        // Duplicate those at 0 to 8, and then move them to 6
        working[8] = population[0];
        working[6] += population[0];

        // Copy working array into population array
        for(int i = 0; i < 9; i++)
        {
            population[i] = working[i];
        }
    }

    unsigned long sum = 0;
    for(int d = 0; d < 9; d++) {
        sum += population[d];
    }

    printf("Population at day %lu: %lu\n", numDays, sum);
}