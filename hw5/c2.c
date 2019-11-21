#include <stdio.h>
#include <stdlib.h>

int main() {
    srand(0);

    for (int i = 0; i < 6; i++) {
        printf("%d\n", rand() % 100);
    }
}
