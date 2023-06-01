#include <iostream>
#include <vector>
#include <string>
#include <cstdio>

using namespace std;

void frameToCodes(int* emaArray) {
    printf("E: %d\n", emaArray[0]); //E
    printf("M: %d\n", emaArray[1]); //M
    printf("A: %d\n", emaArray[2]); //A
    //printf("%d\n", emaArray[3]); //PADS

    //18 bit code
    int _18_bit_codes = (emaArray[0]<<13) | (emaArray[1]<<8) | emaArray[2];
    printf("%d\n\n", _18_bit_codes);
    for (int i=17; i>=0; i--) {
         //_18_bit_codes >> i)
         printf("%d", (_18_bit_codes>>i & 1));   
    }
    printf("\n");


}

void parseEma(string str) {
    //printf("%s\n\n", str.c_str());
    int size = str.length();
    int currentStartIndex = 0;
    for(int i=0; i<size; i++) {
        if (str.c_str()[i] == ';' || i == size-1) {
            string frameString = str.substr(currentStartIndex, i-currentStartIndex);
            //printf("%s\n", frameString.c_str());
            currentStartIndex = i+1;
            int fieldStartIndex = 0;
            int emaArray [4];
            int fieldIndex = 0; 
            for (int j=0; j<frameString.length(); j++) {
                if (frameString.c_str()[j] == ',' || j == frameString.length()-1) {
                    string field = frameString.substr(fieldStartIndex, j-fieldStartIndex+1);
                    //printf("%s\n", field.c_str());
                    fieldStartIndex = j+1;
                    emaArray[fieldIndex++] = atoi(field.c_str());
                }
            }
            //TODO: take emaArray and convert to bits. 
            //These bits will be seperated into 3 bit codes that will later be translated to tokens
            frameToCodes(emaArray);
        }
    }
}






int main()
{
    //string str = "TEST STRING";
    //printf("%s\n\n", str.c_str());
    //string str = "5,28,140,64;6,28,145,64;7,28,150,64;8,28,155,64;31,31,255,64;";
    string str = "1,1,1,   0;";
    parseEma(str);
    
    
    return 0;
}