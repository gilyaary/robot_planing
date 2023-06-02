#include <iostream>
#include <vector>
#include <string>
#include <cstdio>

using namespace std;

int addToBits(int* bits, int from, int value, int size);

int main(int argc, char const *argv[])
{
    //printf("TEST BY GIL\n");

    int bits[32];
    //addToBits(bits, from, value, size)
    int from = 0;
    from = addToBits(bits, from, 1, 6); //LSB
    from = addToBits(bits, from, 1, 6); 
    from = addToBits(bits, from, 1, 6); 
    from = addToBits(bits, from, 1, 6);
    from = addToBits(bits, from, 1, 6);
    from = addToBits(bits, from, 1, 2); 

    for (int i=31; i>=0; i--) {
        printf("%d", bits[i]);
    }

    printf("\n\n");

    return 0;
}

int addToBits(int* bits, int from, int value, int size) {
    for (int i=0; i<size; i++) {
        int bit = (value >> i) && 1;
        //printf("Bit: %d\n", bit);
        bits[from + i] = bit;
    }
    return from + size;
}
