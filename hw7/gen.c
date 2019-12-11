#include <stdio.h>
#include <stdlib.h>

int main() {
    int k;
    printf("Seed: ");
    if (scanf("%d", &k) != 1) return 1;

    srand(k);

    while (1) {
        printf(" => [");
        printf("%d", rand() % 100);
        for (int i = 1; i < 6; i++) {
            printf(", %d", rand() % 100);
        }
        printf("]\n");
        printf("Exit? ");
        char hao[2];
        if (scanf("%s", hao) < 0 || hao[0] == 'y') {
            printf("Byebye\n");
            break;
        }
    }
}
