#include <stdio.h>

int main() {
    FILE *fp = fopen("data.json", "r");

    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    int l1, l2, l3, l4, emergency;

    fscanf(fp, "{\"lane1\":%d,\"lane2\":%d,\"lane3\":%d,\"lane4\":%d,\"emergency\":%d}",
           &l1, &l2, &l3, &l4, &emergency);

    fclose(fp);

    int max = l1;
    int lane = 1;

    if (l2 > max) { max = l2; lane = 2; }
    if (l3 > max) { max = l3; lane = 3; }
    if (l4 > max) { max = l4; lane = 4; }

    if (emergency == 1) {
        printf(" Emergency → GREEN\n");
    } else {
        printf(" Green Signal Lane: %d\n", lane);
    }

    return 0;
}