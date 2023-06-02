#include <iostream>
#include <vector>
#include <string>
#include <cstdio>

using namespace std;

int addToBits(int* bits, int to, int value, int size);
void parseEma(string str);
void frameToCodes(int* emaArray);
int getToken(int code);


int getToken(int code) {
    //000 -> 101110 
    //001 -> 101111
    //010 -> 110111
    //011 -> 101101
    //100 -> 111110
    //101 -> 110110
    //110 -> 111011
    //111 -> 111101
    switch (code){
        case 0: return 46;
        case 1: return 47;
        case 2: return 55;
        case 3: return 45;
        case 4: return 62;
        case 5: return 54;
        case 6: return 59;
        case 7: return 61;
    }
    return 0; //code | (code<<3);
}

void frameToCodes(int* emaArray) {
    //printf("E: %d\n", emaArray[0]); //E
    //printf("M: %d\n", emaArray[1]); //M
    //printf("A: %d\n", emaArray[2]); //A
    //printf("%d\n", emaArray[3]); //PADS

    //18 bit code
    int _18_bit_codes = (emaArray[0]<<13) | (emaArray[1]<<8) | emaArray[2];
    //printf("%d\n\n", _18_bit_codes);
    for (int i=17; i>=0; i--) {
         //_18_bit_codes >> i)
         //printf("%d", (_18_bit_codes>>i & 1));   
    }
    //printf("\n");

    //long tokensValue = 0;
    int SYNC_1_TOKEN = 42; //0x00101010b;
    int SYNC_2_TOKEN = 43; //0x00101011b;
    int TOKEN_SIZE = 6;
    int EXT_SIZE = 2;
    int FRAME_PADS = 10;
    int PHASE_PADS = 0;
    int FRAME_SIZE = 10 * TOKEN_SIZE + 2 * EXT_SIZE + FRAME_PADS + PHASE_PADS;  
    
    int bits [FRAME_SIZE];
    for (int i=0; i<FRAME_SIZE; i++){
        bits[i] = 0;
    }
    int to = FRAME_SIZE-1;
    
    //Phase 1
    to = addToBits(bits, to, SYNC_1_TOKEN, TOKEN_SIZE);
    int phase1CodeTotal = 0;
    for(int i=0; i<9; i+=3) {
        //replace a 3 bitcode for 6 bit toen
        int code = (_18_bit_codes>>i) & 7;
        phase1CodeTotal += code;
        //printf("Code: %d\n", code);
        int token = getToken(code);
        to = addToBits(bits, to, token, TOKEN_SIZE);
    }
    int phase1ErrorCode = phase1CodeTotal%2 == 0 ? 45 : 61;
    
    to = addToBits(bits, to, phase1ErrorCode, TOKEN_SIZE);
    to = addToBits(bits, to, 2, EXT_SIZE); //phase ext 1,0
    to = addToBits(bits, to, 0, PHASE_PADS); //4 pads
    
    //Phase 2
    to = addToBits(bits, to, SYNC_2_TOKEN, TOKEN_SIZE);
    int phase2CodeTotal = 0;
    for(int i=9; i<18; i+=3) {
        //replace a 3 bitcode for 6 bit toen
        int code = (_18_bit_codes>>i) & 7;
        phase2CodeTotal += code;
        //printf("Code: %d\n", code);
        int token = getToken(code);
        to = addToBits(bits, to, token, TOKEN_SIZE); //LSB
    }
    int phase2ErrorCode = phase2CodeTotal%2 == 0 ? 45 : 61;
    to = addToBits(bits, to, phase2ErrorCode, 6);
    to = addToBits(bits, to, 2, EXT_SIZE); //phase ext 1,0
    to = addToBits(bits, to, 0, FRAME_PADS); //4 pads
    int totalBitCount = to;
     
    for (int i=FRAME_SIZE-1; i>=0; i--) {
        printf("%d", bits[i]);
    }
    /*
    to create bytes we need the sync token, the 3 data tokens, the error token and the phase extender + padding
    SYNC DT1 DT2 DT3 ERR EXT PAD
    */
    printf("\n");


}

int addToBits(int* bits, int to, int value, int size) {
    for (int i=0; i<size; i++) {
        int bit = (value >> i) & 1;
        //printf("Bit: %d\n", bit);
        int index = to - size + i + 1;
        //printf("Index: %d\n", index);
        bits[index] = bit;
    }
    return to - size;
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
    string str = "5,28,140,64;6,28,145,64;7,28,150,64;8,28,155,64;31,31,255,64;";
    //string str = "1,1,1,   0;";
    parseEma(str);
    
    
    return 0;
}