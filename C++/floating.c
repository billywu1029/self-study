#include <stdio.h>
#include <stdlib.h> // For exit() function
#include <string.h> // for atof, atoi, and strcat

// 1 << 22 aka 2^22, used to select the 23rd bit in a hex number
// On each iteration, it will be >> 1, to select all bits till the 0th bit
#define MANTISSA_MASK_START 4194304
#define BUF_SIZE 1000 // Default buffer size, should fit all mantissa etc bits
#define BIAS 127
#define NUM_INPUTS 7

union float_bits {
  float f;
  unsigned int bits;
};

// print hex( 5.Of ) outputs "The float looks like Ox4OaOOOOO in hex."
void print_hex( float f) {
  union float_bits t;
  t.f = f;
  printf( "The float looks like 0x%x in hex.\n", t.bits );
}

int is_negative(unsigned int bits) {
  // 1 if negative, 0 o/w
  // Return whether the MSB is set, (left shift a bit by 31)
  return (bits & (1 << (sizeof(int) * 8 - 1))) ? 1 : 0;
}

unsigned int mantissa_bits(unsigned int bits) {
  // Returns the mantissa bits in hex format (0-22th bits, inclusive)
  int mask = 0x7FFFFF;
  return bits & mask; 
}

int extract_exponent(unsigned int bits) {
  // Returns the exponent bits in the 23rd-30th (0-indexed, inclusive) indices
  return ((bits & 0x7F800000) >> 23) - BIAS;
}

void hex_to_binary(char* dest, unsigned int bits) {
  // Copies the string of binary bits from most significant set bit 
  // to the lsb, result won't include a '0b' prefix. (mssetb 0-indexed)
  // Adding '1.' here to fullfill the mantissa bit full binary number
  dest[0] = '1';
  dest[1] = '.';
  char* p = dest + 2; // to make adding char at a time more efficient (vs strcat)
  
  // Choosing z to start at 1 << 22, to select bits one at a time
  for (int z = MANTISSA_MASK_START; z > 0; z >>= 1) {
    *p++ = (bits & z) ? '1' : '0';
  }
  *p = '\0';
}

void construct_rep(char* dest, int is_neg, unsigned int mantissa_t, int exp) {
  char mantissa_binary[BUF_SIZE];
  hex_to_binary(mantissa_binary, mantissa_t);
  char sign[BUF_SIZE] = "-";
  if (is_neg) {
    sprintf(dest, "%s%s * 2^%d\n", sign, mantissa_binary, exp);
  }
  else {
    sprintf(dest, "%s * 2^%d\n", mantissa_binary, exp);
  }
}

int main(void) {
  char infname[] = "floating_in.txt";
  FILE *infile = fopen(infname, "r");

  if (infile == NULL) {
    printf("Error opening file!");
    exit(1);
  }

  size_t len = 0;
  // NOTE: If must use getline, then pass in a preallocated buffer to avoid mem leaks
  // Also, probably better to use fscan/fprintf here for file io
  char *next_line = NULL;
  getline(&next_line, &len, infile);
  int N = atoi(next_line);

  char result[BUF_SIZE];
  union float_bits t;

  for (int j = 0; j < N; j++) {
    getline(&next_line, &len, infile);
    t.f = atof(next_line);
    int is_neg = is_negative(t.bits);
    unsigned int mantissa_t = mantissa_bits(t.bits);
    int exp = extract_exponent(t.bits);
    construct_rep(result, is_neg, mantissa_t, exp);
    print_hex(t.f);
    printf("%s\n", result);
  }

  free(next_line);  // Since getline malloc/reallocs for to fit inp line
  fclose(infile);
}
