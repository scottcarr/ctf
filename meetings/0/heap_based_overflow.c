#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

#define MAX_LEN 64
#define STDIN 0

#define PAGEADDR(addr) (void*)(((int)addr)&0xfffff000)

typedef struct {
	char buf[MAX_LEN];
	int (*cmp)(const char*,const char*);
} vstruct;

int is_foobar_heap(vstruct* s, char* cmp)
{
  int ret;
  strcpy(s->buf, cmp);
  ret = s->cmp(s->buf, "foobar\n");
  return ret;
}

int main()
{
  char *buf = (char*)malloc(MAX_LEN*2);
  int file = open("my_fancy_image", 0);
  int ret = read(file, buf, 2*MAX_LEN);
  printf("Read %d bytes (buffer is %d long)\n", ret, MAX_LEN);

  vstruct *foo = (vstruct*)malloc(sizeof(vstruct));
  printf("Vulnerable buffer starts at %p\n", foo);

  /* make page executable. a real exploit would need some return based
     programming to achieve this, we don't go through that hurdle */
  ret = mprotect(PAGEADDR(foo), 2*MAX_LEN, PROT_READ | PROT_WRITE | PROT_EXEC);
  if (ret!=0) printf("mprotect: %d\n", ret);

  foo->cmp = &strcmp;
  if (is_foobar_heap(foo, buf) == 0) {
    printf("Yes, the file 'my_fancy_image' contains 'foobar'\n");
  }

  free(foo);

  return 1;
}

/* length of buffer is 64.

   shellcode is 31 bytes
   leaves us 33 bytes for the nop slide before that

   shellcode: nop_before nop_after nr_bogus ptr nr_bogus
   shellcode 33 0 0 0x12345678 0
 */
