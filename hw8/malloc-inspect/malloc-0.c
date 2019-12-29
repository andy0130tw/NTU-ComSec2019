#include <stdio.h>
#include <stdlib.h>

int main() {
  void* m0 = malloc(0);
  void* m1 = malloc(0);
  void* m2 = malloc(1);
  printf("Allocated 0 at %p\n", m0);
  printf("Allocated 0 at %p\n", m1);
  printf("Allocated 1 at %p\n", m2);

  free(m0);

}
